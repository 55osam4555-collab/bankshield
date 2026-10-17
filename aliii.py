import streamlit as st  # pyright: ignore[reportMissingImports]
import google.generativeai as genai # pyright: ignore[reportMissingImports]

# إعدادات مظهر الصفحة
st.set_page_config(
    page_title="درع الأمان المصرفي | BankShield AI",
    page_icon="🛡️",
    layout="wide"
)

# تخصيص واجهة باللغة العربية وتصميم حديث
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    h1, h2, h3 { text-align: right; }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=90)
    st.title("🛡️ BankShield AI")
    st.caption("نظام الحماية والإنذار المبكر من الاحتيال المصرفي")
    st.markdown("---")
    
    # إدخال مفتاح الـ API
    api_key = st.text_input("أدخل مفتاح Gemini API الخاص بك:", type="password")
    st.info("💡 يمكنك الحصول على المفتاح مجاناً من aistudio.google.com")
    
    st.markdown("---")
    st.metric(label="إجمالي البلاغات المفحوصة اليوم", value="1,420")
    st.metric(label="محاولات احتيال تم إحباطها", value="389", delta="+12%")

# العنوان الرئيسي
st.title("🛡️ منصة درع الأمان المصرفي")
st.subheader("الكشف الذكي عن رسائل التصيد والاحتيال المالي الموجه للمواطنين")
st.write("قم بلصق نص الرسالة المشبوهة (SMS، واتساب، أو بريد إلكتروني) أو رابط الموقع لتحليله فوراً عبر الذكاء الاصطناعي.")

# حقل إدخال الرسالة
user_input = st.text_area(
    "نص الرسالة أو الرابط المشبوه:",
    placeholder="مثال: عزيزي العميل، تم إيقاف بطاقتك البنكية مؤقتاً لعدم تحديث البيانات. يرجى الاتصال فوراً على الرقم 050XXXXXX أو الدخول على الرابط لتفادي حظر الحساب نهائياً...",
    height=140
)

# دالة تحليل الرسالة عبر الذكاء الاصطناعي
def analyze_scam(text, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    أنت خبير أمن سيبراني متخصص في مكافحة الاحتيال المصرفي والمالي لدى البنك المركزي.
    قم بتحليل الرسالة التالية بدقة وحدد ما إذا كانت محاولة احتيال أو رسالة آمنة:
    
    نص الرسالة:
    \"\"\"{text}\"\"\"
    
    أجب باللغة العربية بالتنسيق التالي بدقة:
    1. **مستوى الخطورة:** (اختر فقط واحدة: [عالي الخطورة 🔴] أو [مشتبه به 🟡] أو [آمن 🟢])
    2. **نوع التهديد:** (مثلاً: انتحال صفة بنك، تصيد احتيالي Phishing، طلب OTP غير مشروع، هندسة اجتماعية، رابط مشبوه)
    3. **الدلائل ومؤشرات الخداع:** (اشرح في 3 نقاط محددة لماذا هذه الرسالة نصابة أو آمنة وما الحيل المستخدمة)
    4. **تعليمات فورية للمواطن:** (خطوات واضحة: ماذا يفعل الآن؟ مثل: لا تضغط، لا تشارك الـ OTP، اتصل برقم البنك الرسمي خلف البطاقة)
    """
    
    response = model.generate_content(prompt)
    return response.text

# زر التحليل
if st.button("🔍 فحص الرسالة والتحقق الآن", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ يرجى إدخال مفتاح Gemini API في الشريط الجانبي أولاً.")
    elif not user_input.strip():
        st.warning("⚠️ يرجى لصق نص الرسالة أولاً قبل الفحص.")
    else:
        with st.spinner("جاري فحص محتوى الرسالة، الأنماط اللغوية، ومؤشرات الاحتيال..."):
            try:
                result = analyze_scam(user_input, api_key)
                st.success("تم اكتمال الفحص الأمني بنجاح!")
                st.markdown("### 📋 نتيجة الفحص والتقرير الأمني:")
                st.markdown(result)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الفحص: {str(e)}")