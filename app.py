import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime

st.set_page_config(page_title="Trikaal Kundli - त्रिकाल कुंडली", page_icon="🕉️")

st.title("🕉️ Trikaal Kundli (त्रिकाल कुंडली)")
st.caption("मूल्यांक विश्लेषण एवं संपूर्ण रिपोर्ट")

# 1 से 9 तक के मूल्यांक का पूरा डेटाबेस
MULANK_DATA = {
    1: {
        "lord": "सूर्य", "dates": "1, 10, 19, 28", "rashi": "सिंह",
        "days": "रविवार, सोमवार", "color": "लाल, नारंगी, सुनहरा", "gem": "माणिक्य (Ruby)",
        "number": "1, 10, 19, 28", "metal": "तांबा, सोना", "mantra": "ॐ घृणिः सूर्याय नमः",
        "strengths": "नेतृत्व क्षमता, आत्मविश्वासी, स्वाभिमानी",
        "weakness": "अहंकार, गुस्सा, जल्दबाजी",
        "remedy": "सूर्य देव को जल चढ़ाएं, पिता का सम्मान करें।"
    },
    2: {
        "lord": "चन्द्रमा", "dates": "2, 11, 20, 29", "rashi": "कर्क",
        "days": "सोमवार, शुक्रवार", "color": "सफेद, क्रीम, सिल्वर", "gem": "मोती (Pearl)",
        "number": "2, 11, 20, 29", "metal": "चाँदी", "mantra": "ॐ सोम सोमाय नमः",
        "strengths": "संवेदनशील, शांत, कल्पनाशील, सहयोगी",
        "weakness": "भावुक होना, ओवरथिंकिंग, मूड स्विंग्स",
        "remedy": "शिवजी की पूजा करें, सोमवार को दूध/पानी दान करें।"
    },
    3: {
        "lord": "बृहस्पति (गुरु)", "dates": "3, 12, 21, 30", "rashi": "धनु, मीन",
        "days": "गुरुवार", "color": "पीला, केसरिया", "gem": "पुखराज (Yellow Sapphire)",
        "number": "3, 12, 21, 30", "metal": "सोना, पीतल", "mantra": "ॐ ब्रं बृहस्पतये नमः",
        "strengths": "ज्ञानी, सलाहकार, अनुशासनप्रिय",
        "weakness": "अत्यधिक आत्मविश्वास, फिजूलखर्ची",
        "remedy": "केले के पेड़ की पूजा करें, बड़ों का आशीर्वाद लें।"
    },
    4: {
        "lord": "राहु", "dates": "4, 13, 22, 31", "rashi": "कन्या (प्रतीकात्मक)",
        "days": "रविवार, शनिवार", "color": "नीला, ग्रे", "gem": "गोमेद (Gomed)",
        "number": "4, 13, 22, 31", "metal": "अष्टधातु", "mantra": "ॐ रां राहवे नमः",
        "strengths": "रचनात्मक, व्यावहारिक, क्रांतिकारी सोच",
        "weakness": "अचानक गुस्सा, भ्रमित रहना",
        "remedy": "सफाई कर्मचारियों की मदद करें, पक्षियों को बाजरा दें।"
    },
    5: {
        "lord": "बुध", "dates": "5, 14, 23", "rashi": "मिथुन, कन्या",
        "days": "बुधवार, शुक्रवार", "color": "हरा, हल्का पीला", "gem": "पन्ना (Emerald)",
        "number": "5, 14, 23", "metal": "कांसा, सोना", "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "strengths": "बुद्धिमान, कम्यूनिकेशन, बिजनेस माइंडेड",
        "weakness": "चंचलता, जल्दी बोर होना, अधीरता",
        "remedy": "गाय को हरी घास खिलाएं, गणेश जी को दूर्वा चढ़ाएं।"
    },
    6: {
        "lord": "शुक्र", "dates": "6, 15, 24", "rashi": "वृष, तुला",
        "days": "शुक्रवार", "color": "सफेद, गुलाबी, चमकीला", "gem": "हीरा (Diamond), ओपल",
        "number": "6, 15, 24", "metal": "चाँदी, प्लैटिनम", "mantra": "ॐ शुं शुक्राय नमः",
        "strengths": "कलात्मक, आकर्षक, शांतिप्रिय",
        "weakness": "आरामपसंदीदा, अत्यधिक दिखावा",
        "remedy": "लक्ष्मी माता की पूजा करें, इत्र का प्रयोग करें।"
    },
    7: {
        "lord": "केतु", "dates": "7, 16, 25", "rashi": "मीन (प्रतीकात्मक)",
        "days": "रविवार, गुरुवार", "color": "मल्टीकलर, हल्का हरा", "gem": "लहसुनिया (Cat's Eye)",
        "number": "7, 16, 25", "metal": "पंचधातु", "mantra": "ॐ कें केतवे नमः",
        "strengths": "शोधकर्ता, आध्यात्मिक, विश्लेषणात्मक",
        "weakness": "अकेलापन, मन में चिंता",
        "remedy": "कुत्ते को रोटी खिलाएं, गणेश जी की आराधना करें।"
    },
    8: {
        "lord": "शनि", "dates": "8, 17, 26", "rashi": "मकर, कुंभ",
        "days": "शनिवार", "color": "काला, गहरा नीला", "gem": "नीलम (Blue Sapphire)",
        "number": "8, 17, 26", "metal": "लोहा", "mantra": "ॐ शं शनैश्चराय नमः",
        "strengths": "मेहनती, धैर्यवान, न्यायप्रिय",
        "weakness": "धीमी प्रगति, निराशावादी सोच",
        "remedy": "शनिवार को पीपल के पेड़ तले दीपक जलाएं, गरीबों की सेवा करें।"
    },
    9: {
        "lord": "मंगल", "dates": "9, 18, 27", "rashi": "मेष, वृश्चिक",
        "days": "मंगलवार", "color": "लाल, गहरा लाल", "gem": "मूंगा (Coral)",
        "number": "9, 18, 27", "metal": "तांबा", "mantra": "ॐ अं अंगारकाय नमः",
        "strengths": "साहसी, ऊर्जावान, निडर",
        "weakness": "अत्यधिक गुस्सा, आक्रामकता",
        "remedy": "हनुमान जी की पूजा करें, हनुमान चालीसा का पाठ करें।"
    }
}

# मूल्यांक निकालने का फंक्शन
def calculate_mulank(date_obj):
    day = date_obj.day
    while day > 9:
        day = sum(int(digit) for digit in str(day))
    return day

# PDF जनरेट करने का फंक्शन
def generate_pdf(name, dob, tob_str, place, mulank, data):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # PDF Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, 750, "TRIKAAL KUNDLI REPORT")
    p.line(50, 735, 550, 735)
    
    # User Details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 700, f"Name: {name}")
    p.drawString(50, 680, f"Date of Birth: {dob.strftime('%d/%m/%Y')}")
    p.drawString(50, 660, f"Time of Birth: {tob_str}")
    p.drawString(50, 640, f"Place of Birth: {place}")
    p.drawString(50, 620, f"Mulank (Lucky Number): {mulank}")
    
    p.line(50, 600, 550, 600)
    
    # Mulank Details
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 570, f"Mulank {mulank} Analysis (Ruler: {data['lord']}):")
    
    p.setFont("Helvetica", 11)
    p.drawString(70, 540, f"- Lucky Dates: {data['dates']}")
    p.drawString(70, 520, f"- Rashi: {data['rashi']}")
    p.drawString(70, 500, f"- Lucky Days: {data['days']}")
    p.drawString(70, 480, f"- Lucky Colors: {data['color']}")
    p.drawString(70, 460, f"- Gemstone: {data['gem']}")
    p.drawString(70, 440, f"- Strengths: {data['strengths']}")
    p.drawString(70, 420, f"- Weakness: {data['weakness']}")
    p.drawString(70, 400, f"- Remedy: {data['remedy']}")
    
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(200, 50, "Generated by Trikaal Kundli App")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# फॉर्म डिज़ाइन
with st.form("kundali_form"):
    name = st.text_input("पूरा नाम (Full Name)")
    
    dob = st.date_input(
        "जन्म तिथि (Date of Birth)", 
        format="DD/MM/YYYY",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today()
    )
    
    st.write("**जन्म समय (Time of Birth)**")
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        hour = st.selectbox("Hour", [f"{i:02d}" for i in range(1, 13)])
    with t_col2:
        minute = st.selectbox("Minute", [f"{i:02d}" for i in range(0, 60)])
    with t_col3:
        ampm = st.selectbox("AM/PM", ["AM", "PM"])
        
    tob_str = f"{hour}:{minute} {ampm}"
    
    place = st.text_input("जन्म स्थान (Birth Place)")
    submit = st.form_submit_button("🔮 विश्लेषण देखें")

# आउटपुट एवं PDF डाउनलोड एक्शन
if submit:
    if not name or not place:
        st.warning("कृपया अपना नाम और जन्म स्थान दर्ज करें।")
    else:
        mulank = calculate_mulank(dob)
        data = MULANK_DATA.get(mulank, MULANK_DATA[1])
        
        st.success(f"✨ {name} जी! आपका **मूल्यांक {mulank}** है।")
        
        # स्क्रीन पर डिटेल्स दिखाना
        st.markdown(f"### 🌟 **मूल्यांक {mulank} - {data['lord']} का प्रभाव**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"📅 **जन्म तारीखें:** {data['dates']}")
            st.write(f"🪐 **स्वामी ग्रह:** {data['lord']}")
            st.write(f"♈ **राशि:** {data['rashi']}")
            st.write(f"🎁 **शुभ दिन:** {data['days']}")
            st.write(f"🎨 **शुभ रंग:** {data['color']}")
            st.write(f"💎 **शुभ रत्न:** {data['gem']}")
        
        with col_b:
            st.write(f"🔢 **शुभ अंक:** {data['number']}")
            st.write(f"🪙 **शुभ धातु:** {data['metal']}")
            st.write(f"🪷 **शुभ मंत्र:** `{data['mantra']}`")
            st.write(f"💡 **विशेषताएं:** {data['strengths']}")
            st.write(f"⚠️ **कमजोरी:** {data['weakness']}")
            st.write(f"✅ **उपाय:** {data['remedy']}")

        # PDF जनरेट करके डाउनलोड बटन दिखाना
        st.markdown("---")
        pdf_bytes = generate_pdf(name, dob, tob_str, place, mulank, data)
        
        st.download_button(
            label="📄 डाउनलोड करें - Trikaal Kundli PDF",
            data=pdf_bytes,
            file_name=f"{name}_Trikaal_Kundli.pdf",
            mime="application/pdf"
        )
