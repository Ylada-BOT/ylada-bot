#!/usr/bin/env python3
"""
Script para gerar ícones PWA a partir do logo existente
"""
from PIL import Image
import os
from pathlib import Path

# Tamanhos de ícones necessários para PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons():
    """Gera ícones PWA em diferentes tamanhos"""
    # Caminhos
    base_dir = Path(__file__).resolve().parent.parent
    logo_path = base_dir / 'web' / 'static' / 'assets' / 'logo.png'
    icons_dir = base_dir / 'web' / 'static' / 'icons'
    
    # Cria diretório de ícones se não existir
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Verifica se o logo existe
    if not logo_path.exists():
        print(f"❌ Logo não encontrado em: {logo_path}")
        print("💡 Criando ícone padrão...")
        # Cria um ícone padrão simples
        create_default_icon(icons_dir)
        return
    
    try:
        # Abre o logo original
        logo = Image.open(logo_path)
        
        # Converte para RGBA se necessário
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        print(f"✅ Logo encontrado: {logo_path}")
        print(f"📐 Tamanho original: {logo.size}")
        
        # Gera ícones em diferentes tamanhos
        for size in ICON_SIZES:
            # Redimensiona mantendo proporção
            icon = logo.resize((size, size), Image.Resampling.LANCZOS)
            
            # Salva o ícone
            icon_path = icons_dir / f'icon-{size}x{size}.png'
            icon.save(icon_path, 'PNG', optimize=True)
            print(f"✅ Criado: {icon_path.name}")
        
        print(f"\n🎉 Todos os ícones foram gerados em: {icons_dir}")
        
    except Exception as e:
        print(f"❌ Erro ao processar logo: {e}")
        print("💡 Criando ícone padrão...")
        create_default_icon(icons_dir)

def create_default_icon(icons_dir):
    """Cria um ícone padrão simples se o logo não existir"""
    from PIL import ImageDraw
    
    for size in ICON_SIZES:
        # Cria imagem com fundo gradiente
        icon = Image.new('RGBA', (size, size), (59, 130, 246, 255))  # Azul
        draw = ImageDraw.Draw(icon)
        
        # Desenha um círculo com borda
        margin = size // 10
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=(139, 92, 246, 255),  # Roxo
            outline=(255, 255, 255, 255),
            width=max(2, size // 32)
        )
        
        # Adiciona texto "Y" no centro
        try:
            from PIL import ImageFont
            # Tenta usar fonte padrão
            font_size = size // 2
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            # Fallback para fonte padrão
            font = ImageFont.load_default()
        
        # Calcula posição do texto
        text = "Y"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        draw.text(position, text, fill=(255, 255, 255, 255), font=font)
        
        # Salva
        icon_path = icons_dir / f'icon-{size}x{size}.png'
        icon.save(icon_path, 'PNG', optimize=True)
        print(f"✅ Criado ícone padrão: {icon_path.name}")

if __name__ == '__main__':
    print("🎨 Gerando ícones PWA...\n")
    generate_icons()


