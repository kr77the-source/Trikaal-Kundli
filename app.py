import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import datetime

st.set_page_config(page_title="Trikaal Kundli - त्रिकाल कुंडली", page_icon="🕉️")

st.title("🕉️ Trikaal Kundli (त्रिकाल कुंडली)")
st.caption("मूल्यांक विश्लेषण एवं संपूर्ण रिपोर्ट")

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
    5: {
        "lord": "बुध", "dates": "5, 14, 23", "rashi": "मिथुन, कन्या",
        "days": "बुधवार, शुक्रवार", "color": "हरा, हल्का पीला", "gem": "पन्ना (Emerald)",
        "number": "5, 14, 23", "metal": "कांसा, सोना", "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "strengths": "बुद्धिमान, कम्यूनिकेशन, बिजनेस माइंडेड",
        "weakness": "चंचलता, जल्दी बोर होना, अधीरता",
        "remedy": "गाय को हरी घास खिलाएं, गणेश जी को दूर्वा चढ़ाएं।"
    }
}

def calculate_mulank(date_obj):
    day = date_obj.day
    while day > 9:
        day = sum(int(digit) for digit in str(day))
    return day

with st.form("kundali_form"):
    name = st.text_input("पूरा नाम (Full Name)")
    
    # 1900 से लेकर आज तक की डेट रेंज के साथ input
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

if submit:
    if not name or not place:
        st.warning("कृपया अपना नाम और जन्म स्थान दर्ज करें।")
    else:
        mulank = calculate_mulank(dob)
        data = MULANK_DATA.get(mulank, MULANK_DATA[5])
        
        st.success(f"✨ {name} जी! आपका जन्म समय **{tob_str}** है और आपका **मूल्यांक {mulank}** है।")
        
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
            st.write(f"🔢 **भाग्यांक/शुभ अंक:** {data['number']}")
            st.write(f"🪙 **शुभ धातु:** {data['metal']}")
            st.write(f"🪷 **शुभ मंत्र:** `{data['mantra']}`")
            st.write(f"💡 **विशेषताएं:** {data['strengths']}")
            st.write(f"⚠️ **कमजोरी:** {data['weakness']}")
            st.write(f"✅ **उपाय:** {data['remedy']}")
