import os
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

COOKIE_PATH = "tiktok_cookies.json"

async def get_recent_posts(username: str, limit: int = 10) -> list:
    clean_username = username if username.startswith("@") else f"@{username}"
    target_url = f"https://www.tiktok.com/{clean_username}"

    if not os.path.exists(COOKIE_PATH):
        raise FileNotFoundError(f"Archivo de sesión '{COOKIE_PATH}' no encontrado.")

    print(f"Extrayendo métricas y descripciones de los últimos {limit} videos de {clean_username}...")
    posts_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            storage_state=COOKIE_PATH,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await page.goto(target_url, wait_until="domcontentloaded")
        
        try:
            await page.wait_for_selector('div[data-e2e="user-post-item"]', timeout=60000)
            await page.wait_for_timeout(2000) 
        except Exception as e:
            print(f"[ALERTA] No se encontró la cuadrícula de videos. Error: {e}")
            await browser.close()
            return posts_data

        video_count = await page.locator('div[data-e2e="user-post-item"]').count()
        actual_limit = min(limit, video_count)

        if actual_limit == 0:
            print("No se encontraron videos públicos.")
            await browser.close()
            return posts_data

        for i in range(actual_limit):
            try:
                # Clic orgánico en la miniatura
                await page.locator('div[data-e2e="user-post-item"] a').nth(i).click()

                # Esperamos el modal del video
                await page.wait_for_selector('strong[data-e2e="browse-like-count"]', timeout=15000)
                await page.wait_for_timeout(1000)
                
                current_url = page.url
                post_html = await page.content()
                post_soup = BeautifulSoup(post_html, "html.parser")

                # Buscamos métricas
                like_btn = post_soup.find("strong", {"data-e2e": "browse-like-count"})
                comment_btn = post_soup.find("strong", {"data-e2e": "browse-comment-count"})
                fav_btn = post_soup.find("strong", {"data-e2e": "browse-favorite-count"})
                
                # Buscamos la descripción escrita (caption)
                desc_element = post_soup.find(attrs={"data-e2e": "browse-video-desc"})
                
                likes_val = like_btn.text.strip() if like_btn else "0"
                comments_val = comment_btn.text.strip() if comment_btn else "0"
                favs_val = fav_btn.text.strip() if fav_btn else "0"
                text_val = desc_element.text.strip().replace('\n', ' ') if desc_element else ""
                
                posts_data.append({
                    "url": current_url,
                    "likes": likes_val,
                    "comments": comments_val,
                    "favorites": favs_val,
                    "text": text_val
                })
                
            except Exception as e:
                print(f"  -> Error en la extracción del video {i+1}: {e}")

            # Retornar al perfil principal
            await page.goto(target_url, wait_until="domcontentloaded")
            await page.wait_for_selector('div[data-e2e="user-post-item"]', timeout=15000)
            await page.wait_for_timeout(1500)

        await browser.close()
        
    return posts_data