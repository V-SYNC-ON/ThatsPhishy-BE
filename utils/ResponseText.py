statuses = {
    "English": {
        "risky": "risky",
        "not recommended": "not recommended",
        "safe": "safe"
    },
    "Korean": {
        "risky": "위험",
        "not recommended": "비권장",
        "safe": "안전"
    },
    "Japanese": {
        "risky": "危険",
        "not recommended": "非推奨",
        "safe": "安全"
    },
    "Tamil": {
        "risky": "ஆபத்துக்குரிய",
        "not recommended": "பரிந்துரைக்கப்படாதது",
        "safe": "பாதுகாப்பான"
    },
    "Telugu": {
        "risky": "ప్రమాదకరమైన",
        "not recommended": "సిఫార్షు చేయబడదు",
        "safe": "సురక్షితం"
    },
    "Hindi": {
        "risky": "जोखिमपूर्ण",
        "not recommended": "सिफारिश नहीं की जाती",
        "safe": "सुरक्षित"
    }
}

def generate_description(language, status, domain):
    descriptions = {
        "English": {
            "risky": f"This website {domain} exhibits a concerning security profile, that could potentially impact your online security.",
            "not recommended": f"This website {domain} exhibits an ordinary security profile, with moderate but manageable risks to your online security.",
            "safe": f"This website {domain} is considered safe and poses no apparent risks to your online security.",
            "error": "Something went wrong",
            "not_found": "URL doesn't exist"
        },
        "Korean": {
            "risky": f"이 웹사이트 {domain}은(는) 우려되는 보안 프로필을 보여주며 온라인 보안에 잠재적으로 영향을 미칠 수 있습니다.",
            "not recommended": f"이 웹사이트 {domain}은(는) 평범한 보안 프로필을 보여주며, 온라인 보안에 중간 정도의 관리 가능한 위험이 있습니다.",
            "safe": f"이 웹사이트 {domain}은(는) 안전하다고 간주되며 온라인 보안에 명백한 위험이 없습니다.",
            "error": "문제가 발생했습니다",
            "not_found": "URL이 존재하지 않습니다"
        },
        "Japanese": {
            "risky": f"このウェブサイト{domain}は懸念すべきセキュリティプロファイルを示し、オンラインセキュリティに潜在的な影響を及ぼす可能性があります。",
            "not recommended": f"このウェブサイト{domain}は普通のセキュリティプロファイルを示し、オンラインセキュリティには中程度のリスクがあるものの、管理可能です。",
            "safe": f"このウェブサイト{domain}は安全と見なされ、オンラインセキュリティに明らかなリスクはありません。",
            "error": "何かがうまくいかなかった",
            "not_found": "URLが存在しません"
        },
        "Tamil": {
            "risky": f"இந்த வலைத்தளம் {domain} ஒரு அச்சிடுதல் பரிசோதனை பட்டியலை காட்டுகின்றது, உங்கள் இணைய பாதுகாப்பிற்கு உத்தமமாக பாதிக்கலாம்.",
            "not recommended": f"இந்த வலைத்தளம் {domain} சாதாரண பாதுகாப்பு பரிசோதனையைக் காட்டுகின்றது, மெதுவான ஆனால் மேலும் உத்தமமாக பொருள்கள் உள்ளன.",
            "safe": f"இந்த வலைத்தளம் {domain} பாதுகாப்பு தான் என்பது எளிதில் கொள்ளப்பட்டு உங்கள் இணைய பாதுகாப்பிற்கு விளக்குகின்றது.",
            "error": "ஏதாவது பிழை ஏற்பட்டுள்ளது",
            "not_found": "URL இல்லை"
        },
        "Telugu": {
            "risky": f"ఈ వెబ్‌సైట్ {domain} చింతనీయ భద్రత ప్రొఫైల్‌ను చూపిస్తుంది, మీ ఆన్‌లైన్ భద్రతకు ప్రభావం చేయవచ్చు.",
            "not recommended": f"ఈ వెబ్‌సైట్ {domain} సామాన్య భద్రత ప్రొఫైల్‌ను చూపిస్తుంది, మీ ఆన్‌లైన్ భద్రతకు మధ్యస్థమైన కష్టాలు ఉన్నాయి కానీ నిర్వహించగలవు.",
            "safe": f"ఈ వెబ్‌సైట్ {domain} ఆపద్‌కరమైనదని చూడడం వలన మీ ఆన్‌లైన్ భద్రతకు ప్రత్యక్షములు లేని ప్రాధాన్యాలు ఉన్నాయి.",
            "error": "ఏది చాలా సరైన కార్యాచరణ లేదు",
            "not_found": "URL ఉనికి లేదు"
        },
        "Hindi": {
            "risky": f"इस वेबसाइट {domain} का एक चिंताजनक सुरक्षा प्रोफ़ाइल दिखाता है, जो आपके ऑनलाइन सुरक्षा पर प्रत्याशित रूप से प्रभाव डाल सकता है।",
            "not recommended": f"इस वेबसाइट {domain} एक सामान्य सुरक्षा प्रोफ़ाइल दिखाता है, जिसमें मध्यम से मध्यम परियाप्त सुरक्षा के खतरे हैं।",
            "safe": f"इस वेबसाइट {domain} को सुरक्षित माना जाता है और ऑनलाइन सुरक्षा पर कोई स्पष्ट खतरा नहीं होता है।",
            "error": "कुछ गड़बड़ हो गई",
            "not_found": "URL मौजूद नहीं है"
        }
    }

    return descriptions.get(language, {}).get(status, f"Unknown status for website {domain} in {language}.")
