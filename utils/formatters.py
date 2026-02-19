from api.models.specialty import Specialty
from api.models.info_section import InfoSection, InfoBlock

def format_specialty(spec: Specialty) -> str:
    text = f"<b>{spec.code} {spec.name}</b>\n\n"
    if spec.description:
        text += f"<b>📌 О специальности</b>\n{spec.description}\n\n"
    if spec.professional_activity:
        text += f"<b>🔧 Профессиональная деятельность</b>\n{spec.professional_activity}\n\n"
    if spec.activities:
        text += f"<b>⚙️ Что делает</b>\n{spec.activities}\n\n"
    if spec.qualities:
        text += f"<b>💪 Качества</b>\n{spec.qualities}\n\n"
    if spec.subjects:
        text += f"<b>📚 Что будет изучать</b>\n{spec.subjects}\n\n"
    if spec.entrance_tests:
        text += f"<b>📝 Вступительные испытания</b>\n{spec.entrance_tests}\n"
    return text

def format_info_section(section: InfoSection) -> str:
    """Форматирует информационный раздел для красивого отображения"""
    lines = []
    
    # Заголовок раздела
    lines.append(f"<b>{section.title}</b>")
    lines.append("")
    
    # Обрабатываем блоки по порядку
    for block in sorted(section.blocks, key=lambda x: x.order):
        if block.block_type == "heading":
            if block.title:
                lines.append(f"\n<b>{block.title}</b>")
                lines.append("")
                
        elif block.block_type == "paragraph":
            if block.content and "text" in block.content:
                lines.append(block.content["text"])
                lines.append("")
                
        elif block.block_type == "list":
            if block.content and "items" in block.content:
                for item in block.content["items"]:
                    lines.append(f"• {item}")
                lines.append("")
                
        elif block.block_type in ["warning", "important"]:
            if block.content and "text" in block.content:
                lines.append(f"⚠️ {block.content['text']}")
                lines.append("")
    
    # Если нет блоков, показываем обычный content
    if not section.blocks and section.content and section.content != ".":
        lines.append(section.content)
    
    return "\n".join(lines)