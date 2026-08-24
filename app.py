import streamlit as st
import datetime
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Trikaal Kundli - त्रिकाल कुंडली", page_icon="🕉️")

st.title("🕉️ Trikaal Kundli (त्रिकाल कुंडली)")
st.caption("मूल्यांक विश्लेषण एवं संपूर्ण रिपोर्ट")

# 1 से 9 तक का डेटा (अंग्रेजी/Hinglish टेक्स्ट का प्रयोग PDF फ़ॉन्ट इश्यू से बचने के लिए)
MULANK_DATA = {
    1: {
        "lord": "Sun (Surya)", "dates": "1, 10, 19, 28", "rashi": "Leo (Simha)",
        "days": "Sunday, Monday", "color": "Red, Orange, Gold", "gem": "Ruby (Manikya)",
        "number": "1, 10, 19, 28", "metal": "Copper, Gold", "mantra": "Om Ghrini Suryaya Namah",
        "strengths": "Leadership, Confident, Self-respecting",
        "weakness": "Ego, Anger, Impatience",
        "remedy": "Offer water to Sun Lord, respect father."
    },
    2: {
        "lord": "Moon (Chandra)", "dates": "2, 11, 20, 29", "rashi": "Cancer (Kark)",
        "days": "Monday, Friday", "color": "White, Cream, Silver", "gem": "Pearl (Moti)",
        "number": "2, 11, 20, 29", "metal": "Silver", "mantra": "Om Som Somaya Namah",
        "strengths": "Sensitive, Calm, Imaginative, Helpful",
        "weakness": "Over-emotional, Overthinking, Mood Swings",
        "remedy": "Worship Lord Shiva, donate milk/water on Mondays."
    },
    5: {
        "lord": "Mercury (Budh)", "dates": "5, 14, 23", "rashi": "Gemini, Virgo",
        "days": "Wednesday, Friday", "color": "Green, Light Yellow", "gem": "Emerald (Panna)",
        "number": "5, 14, 23", "metal": "Bronze, Gold", "mantra": "Om Bram Breem Broum Sah Budhaya Namah",
        "strengths": "Intelligent, Great Communication, Business Minded",
        "weakness": "Restlessness, Gets bored easily, Impatient",
        "remedy": "Feed green grass to cows, offer Durva to Lord Ganesha."
    }
}

def calculate_mulank(date_obj):
    day = date_obj.day
    while day > 9:
        day = sum(int(digit) for digit in str(day))
    return day

# 🎨 बर्थ चार्ट (Lagna Chart Image) बनाने का फंक्शन
def draw_birth_chart():
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Outer Square
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='#8B0000', lw=3)
    # Diagonals
    ax.plot([0, 10], [10, 0], color='#8B0000', lw=1.5)
    ax.plot([0, 10], [0, 10], color='#8B0000', lw=1.5)
    # Inner Diamond
    ax.plot([5, 10, 5, 0, 5], [10, 5, 0, 5, 10], color='#8B0000', lw=2)

    # House Labels (North Indian Style)
    ax.text(5, 7.5, "1 (Lagna)", fontsize=10, ha='center', weight='bold', color='#1A237E')
    ax.text(2.5, 8.8, "2", fontsize=9, ha='center')
    ax.text(1.2, 7.5, "3", fontsize=9, ha='center')
    ax.text(2.5, 5, "4", fontsize=9, ha='center')
    ax.text(1.2, 2.5, "5", fontsize=9, ha='center')
    ax.text(2.5, 1.2, "6", fontsize=9, ha='center')
    ax.text(5, 2.5, "7", fontsize=9, ha='center')
    ax.text(7.5, 1.2, "8", fontsize=9, ha='center')
    ax.text(8.8, 2.5, "9", fontsize=9, ha='center')
    ax.text(7.5, 5, "10", fontsize=9, ha='center')
    ax.text(8.8, 7.5, "11", fontsize=9, ha='center')
    ax.text(7.5, 8.8, "12", fontsize=9, ha='center')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    buf.seek(0)
    plt.close(fig)
    return buf

# 📄 प्रीमियम PDF डिज़ाइन तैयार करने का फंक्शन
def build_stylish_pdf(name, dob, tob_str, place, mulank, data, chart_buf):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor("#1A237E"),
        alignment=1,
        spaceAfter=15
    )
    
    label_style = ParagraphStyle('Label', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#333333"))
    value_style = ParagraphStyle('Value', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#1A237E"))

    # Title
    story.append(Paragraph("TRIKAAL KUNDLI REPORT", title_style))
    story.append(Spacer(1, 10))

    # User Details & Chart Section
    user_info = [
        [Paragraph("<b>Name:</b>", label_style), Paragraph(name, value_style)],
        [Paragraph("<b>Date of Birth:</b>", label_style), Paragraph(dob.strftime('%d/%m/%Y'), value_style)],
        [Paragraph("<b>Time of Birth:</b>", label_style), Paragraph(tob_str, value_style)],
        [Paragraph("<b>Place of Birth:</b>", label_style), Paragraph(place, value_style)],
        [Paragraph("<b>Mulank:</b>", label_style), Paragraph(str(mulank), value_style)],
    ]
    
    info_table = Table(user_info, colWidths=[100, 150])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E0E0E0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1A237E")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))

    chart_img = RLImage(chart_buf, width=170, height=170)

    # Combine Info & Chart side by side
    top_grid = Table([[info_table, chart_img]], colWidths=[270, 270])
    top_grid.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(top_grid)
    story.append(Spacer(1, 20))

    # Mulank Details Table Header
    story.append(Paragraph(f"<b>MULANK {mulank} DETAILS (Ruler: {data['lord']})</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#8B0000"), alignment=1)))
    story.append(Spacer(1, 10))

    # Table like Image
    table_data = [
        [Paragraph("<b>Attribute</b>", label_style), Paragraph("<b>Details</b>", label_style)],
        [Paragraph("Lucky Dates", label_style), Paragraph(data["dates"], value_style)],
        [Paragraph("Ruling Planet", label_style), Paragraph(data["lord"], value_style)],
        [Paragraph("Zodiac (Rashi)", label_style), Paragraph(data["rashi"], value_style)],
        [Paragraph("Lucky Days", label_style), Paragraph(data["days"], value_style)],
        [Paragraph("Lucky Colors", label_style), Paragraph(data["color"], value_style)],
        [Paragraph("Gemstone", label_style), Paragraph(data["gem"], value_style)],
        [Paragraph("Lucky Numbers", label_style), Paragraph(data["number"], value_style)],
        [Paragraph("Metal", label_style), Paragraph(data["metal"], value_style)],
        [Paragraph("Mantra", label_style), Paragraph(data["mantra"], value_style)],
        [Paragraph("Strengths", label_style), Paragraph(data["strengths"], value_style)],
        [Paragraph("Weakness", label_style), Paragraph(data["weakness"], value_style)],
        [Paragraph("Remedy", label_style), Paragraph(data["remedy"], value_style)],
    ]

    mulank_table = Table(table_data, colWidths=[150, 390])
    mulank_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A237E")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#B0BEC5")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(mulank_table)
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

# UI Inputs
with st.form("kundali_form"):
    name = st.text_input("पूरा नाम (Full Name)")
    dob = st.date_input("जन्म तिथि (Date of Birth)", format="DD/MM/YYYY", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    
    st.write("**जन्म समय (Time of Birth)**")
    t1, t2, t3 = st.columns(3)
    with t1: hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    with t2: minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])
    with t3: ampm = st.selectbox("AM/PM", ["AM", "PM"])
    tob_str = f"{hour}:{minute} {ampm}"
    
    place = st.text_input("जन्म स्थान (Birth Place)")
    submit = st.form_submit_button("🔮 विश्लेषण देखें")

if submit:
    if not name or not place:
        st.warning("कृपया नाम और स्थान भरें।")
    else:
        mulank = calculate_mulank(dob)
        data = MULANK_DATA.get(mulank, MULANK_DATA[5])
        
        st.success(f"✨ {name} जी, आपकी कुंडली तैयार है!")
        
        # Display Chart
        chart_buf = draw_birth_chart()
        st.image(chart_buf, caption="Lagna Kundali Chart", width=300)

        # Download PDF Button
        pdf_bytes = build_stylish_pdf(name, dob, tob_str, place, mulank, data, chart_buf)
        st.download_button(
            label="📄 डाउनलोड करें - Premium Kundli PDF",
            data=pdf_bytes,
            file_name=f"{name}_Trikaal_Kundli.pdf",
            mime="application/pdf"
        )
