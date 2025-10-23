"""
Script de testing para generación de artículos de blog
"""
import asyncio
from blog_scheduler import test_generate_article

async def main():
    print("=" * 60)
    print("TEST: Generación de Artículo de Blog")
    print("=" * 60)
    print()
    
    # Generar artículo del día actual
    print("Generando artículo para el día de hoy...")
    print("Esto puede tomar 30-60 segundos...")
    print()
    
    article = await test_generate_article()
    
    if article:
        print()
        print("✅ ARTÍCULO GENERADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"ID: {article.id}")
        print(f"Título: {article.title}")
        print(f"Slug: {article.slug}")
        print(f"Autor: {article.author_name} ({article.author_role})")
        print(f"Publicado: {article.published}")
        print(f"Palabras: {len(article.content.split())}")
        print(f"Tiempo de lectura: {article.reading_time} min")
        print("=" * 60)
        print()
        print("Puedes ver el artículo en:")
        print(f"- API: http://localhost:8001/api/blog/posts")
        if article.published:
            print(f"- Frontend: http://localhost:3000/blog/{article.slug}")
        print()
    else:
        print()
        print("❌ ERROR: No se pudo generar el artículo")
        print("Revisa los logs del backend para más detalles")
        print()

if __name__ == "__main__":
    asyncio.run(main())
