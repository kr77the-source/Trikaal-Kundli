import io
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Flatlib Imports for Astrological Calculations
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Trikaal Kundli - त्रिकाल कुंडली", page_icon="🕉️")

st.title("🕉️ Trikaal Kundli (त्रिकाल कुंडली)")
st.caption("मूल्यांक विश्लेषण एवं संपूर्ण रिपोर्ट")

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

PLANET_SHORT = {
    const.SUN: "Su", const.MOON: "Mo", const.MARS: "Ma",
    const.MERCURY: "Me", const.JUPITER: "Ju", const.VENUS: "Ve",
    const.SATURN: "Sa", const.NORTH_NODE: "Ra", const.SOUTH_NODE: "Ke"
}

RASHI_MAP = {
    const.ARIES: 1, const.TAURUS: 2, const.GEMINI: 3, const.CANCER: 4,
    const.LEO: 5, const.VIRGO: 6, const.LIBRA: 7, const.SCORPIO: 8,
    const.SAGITTARIUS: 9, const.CAPRICORN: 10, const.AQUARIUS: 11, const.PISCES: 12
}

def calculate_mulank(date_obj):
    day = date_obj.day
    while day > 9:
        day = sum(int(digit) for digit in str(day))
    return day

# 🪐 Dynamic Chart Calculation Engine
def compute_kundli_data(dob, hour_24, minute, lat=28.6139, lon=77.2090):
    dt_str = f"{dob.year}/{dob.month:02d}/{dob.day:02d}"
    time_str = f"{hour_24:02d}:{minute:02d}"
    
    pos = GeoPos(lat, lon)
    date_obj = Datetime(dt_str, time_str, '+05:30')
    chart = Chart(date_obj, pos, hsys=const.HOUSES_EQUAL, mode=const.AYANAMSA_LAHIRI)

    asc_rashi = RASHI_MAP[chart.get(const.ASC).sign]
    
    houses_dict = {h: {"rashi": ((asc_rashi + h - 2) % 12) + 1, "planets": []} for h in range(1, 13)}

    for p_id, p_name in PLANET_SHORT.items():
        obj = chart.get(p_id)
        p_rashi = RASHI_MAP[obj.sign]
        h_num = ((p_rashi - asc_rashi) % 12) + 1
        houses_dict[h_num]["planets"].append(p_name)

    return houses_dict

# 🎨 Dynamic Birth Chart Canvas Visualizer
def draw_birth_chart(chart_data):
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Border & House Grid Setup
    ax.plot([0, 10, 10, 0, 0], [0, 0, 10, 10, 0], color='#8B0000', lw=3)
    ax.plot([0, 10], [10, 0], color='#8B0000', lw=1.5)
    ax.plot([0, 10], [0, 10], color='#8B0000', lw=1.5)
    ax.plot([5, 10, 5, 0, 5], [10, 5, 0, 5, 10], color='#8B0000', lw=2)

    # Coordinates for center of each house
    house_coords = {
        1: (5.0, 6.2),  2: (2.5, 8.2),  3: (1.2, 6.5),
        4: (3.0, 5.0),  5: (1.2, 3.5),  6: (2.5, 1.8),
        7: (5.0, 3.8),  8: (7.5, 1.8),  9: (8.8, 3.5),
        10: (7.0, 5.0), 11: (8.8, 6.5), 12: (7.5, 8.2)
    }

    for house_num, info in chart_data.items():
        cx, cy = house_coords[house_num]
        
        # Display Rashi Number
        ax.text(cx, cy + 0.5, str(info["rashi"]), fontsize=10, ha='center', va='center', weight='bold', color='#1A237E')
        
        # Display Planets in House
        if info["planets"]:
            p_text = " ".join(info["planets"])
            ax.text(cx, cy - 0.5, p_text, fontsize=8, ha='center', va='center', weight='bold', color='#B71C1C')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
    buf.seek(0)
    plt.close(fig)
    return buf

# 📄 PDF Builder Function
def build_stylish_pdf(name, dob, tob_str, place, mulank, data, chart_buf):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=22, textColor=colors.HexColor("#1A237E"), alignment=1, spaceAfter=15
    )
    label_style = ParagraphStyle('Label', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#333333"))
    value_style = ParagraphStyle('Value', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#1A237E"))

    story.append(Paragraph("TRIKAAL KUNDLI REPORT", title_style))
    story.append(Spacer(1, 10))

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
    top_grid = Table([[info_table, chart_img]], colWidths=[270, 270])
    top_grid.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(top_grid)
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>MULANK {mulank} DETAILS (Ruler: {data['lord']})</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#8B0000"), alignment=1)))
    story.append(Spacer(1, 10))

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

# Streamlit Interface Form
with st.form("kundali_form"):
    name = st.text_input("पूरा नाम (Full Name)")
    dob = st.date_input("जन्म तिथि (Date of Birth)", format="DD/MM/YYYY", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    
    st.write("**जन्म समय (Time of Birth)**")
    t1, t2, t3 = st.columns(3)
    with t1: hour_12 = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    with t2: minute_str = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])
    with t3: ampm = st.selectbox("AM/PM", ["AM", "PM"])
    tob_str = f"{hour_12}:{minute_str} {ampm}"
    
    place = st.text_input("जन्म स्थान (Birth Place)", value="Delhi")
    submit = st.form_submit_button("🔮 विश्लेषण देखें")

if submit:
    if not name or not place:
        st.warning("कृपया नाम और स्थान भरें।")
    else:
        # Convert Time to 24-Hour Format for Astrological Engine
        h = int(hour_12)
        if ampm == "PM" and h != 12:
            h += 12
        elif ampm == "AM" and h == 12:
            h = 0
        m = int(minute_str)

        mulank = calculate_mulank(dob)
        data = MULANK_DATA.get(mulank, MULANK_DATA[5])

        # Dynamic Chart Processing
        chart_data = compute_kundli_data(dob, h, m)
        chart_buf = draw_birth_chart(chart_data)

        st.success(f"✨ {name} जी, आपकी कुंडली तैयार है!")
        st.image(chart_buf, caption="Lagna Kundali Chart (Real-time Calculation)", width=350)

        pdf_bytes = build_stylish_pdf(name, dob, tob_str, place, mulank, data, chart_buf)
        st.download_button(
            label="📄 डाउनलोड करें - Premium Kundli PDF",
            data=pdf_bytes,
            file_name=f"{name}_Trikaal_Kundli.pdf",
            mime="application/pdf"
        )
