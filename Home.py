import streamlit as st

def main():
  st.set_page_config(page_title="SoulSolace", page_icon="logo.svg", layout="wide", initial_sidebar_state="collapsed")

    # ---------- Modern Styles ----------
  st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    :root{
      --bg-light:#f5f9ff; --bg-white:#ffffff;
      --accent:#8bbffc; --accent-dark:#4a90e2; --accent-glow:rgba(139,191,252,.3);
      --text:#0f172a; --text-muted:#808391; --border:rgba(139,191,252,.2);
      --glass-bg:rgba(255,255,255,.7); --glass-border:rgba(139,191,252,.15);
    }
    
    html,body,[data-testid="stApp"]{
      background: linear-gradient(135deg, #f5f9ff 0%, #e3f0ff 50%, #ffffff 100%);
      font-family: 'Inter', -apple-system, sans-serif;
      color: var(--text);
    }
    
    .block-container{ 
      max-width:1280px; 
      padding-top:3.5rem !important; 
      padding-bottom:3rem;
      animation: fadeIn .6s ease-out;
    }
    
    @keyframes fadeIn{ from{ opacity:0; transform:translateY(20px); } to{ opacity:1; transform:translateY(0); } }
    @keyframes float{ 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(-10px); } }
    @keyframes glow{ 0%,100%{ box-shadow:0 20px 60px rgba(139,191,252,.25), 0 10px 30px rgba(74,144,226,.15); } 
                     50%{ box-shadow:0 25px 70px rgba(139,191,252,.35), 0 15px 40px rgba(74,144,226,.2); } }
    
    /* Hero Section */
    .hero{
      position:relative; overflow:hidden;
      display:flex; gap:40px; align-items:center; 
      padding:60px 48px; margin-bottom:48px; margin-top:20px;
      border-radius:32px;
      background: linear-gradient(135deg, #8bbffc 0%, #a8cffe 50%, #c8e3ff 100%);
      box-shadow: 0 20px 60px rgba(139,191,252,.25), 0 10px 30px rgba(74,144,226,.15);
    }
    
    .hero::before{
      content:''; position:absolute; top:-50%; right:-50%;
      width:100%; height:100%; border-radius:50%;
      background: radial-gradient(circle, rgba(255,255,255,.4) 0%, transparent 70%);
      animation: float 6s ease-in-out infinite;
    }
    
    .hero-content{ position:relative; z-index:1; flex:1; }
    
    .hero h1{ 
      color:#fff; margin:0 0 12px; 
      font-size:clamp(36px,5vw,56px); 
      font-weight:900; 
      letter-spacing:-.03em;
      text-shadow: 0 2px 20px rgba(0,0,0,.3);
    }
    
    .hero .tagline{ 
      color:rgba(255,255,255,.9); 
      font-size:clamp(18px,2vw,24px); 
      font-weight:600; 
      margin:0 0 16px;
      text-shadow: 0 1px 10px rgba(0,0,0,.2);
    }
    
    .hero p{ 
      color:rgba(255,255,255,.85); 
      margin:0 0 28px; 
      font-size:1.1rem; 
      line-height:1.7;
      max-width:600px;
    }
    
    .cta-group{ display:flex; gap:16px; flex-wrap:wrap; }
    
    .btn-primary, .btn-secondary{
      display:inline-flex; align-items:center; gap:8px;
      padding:14px 28px; border-radius:16px;
      font-weight:700; font-size:1rem;
      text-decoration:none; border:0;
      transition: all .3s cubic-bezier(.4,0,.2,1);
      cursor:pointer;
    }
    
    .btn-primary{
      background:#fff; color:var(--accent-dark);
      box-shadow:0 10px 30px rgba(139,191,252,.3);
    }
    
    .btn-primary:hover{
      transform:translateY(-2px) scale(1.02);
      box-shadow:0 15px 40px rgba(139,191,252,.4);
    }
    
    .btn-secondary{
      background:rgba(255,255,255,.5); color:var(--accent-dark);
      backdrop-filter:blur(10px);
      border:1px solid rgba(255,255,255,.4);
    }
    
    .btn-secondary:hover{
      background:rgba(255,255,255,.7);
      transform:translateY(-2px);
    }
    
    /* Section Headers */
    .section-header{ 
      text-align:center; 
      margin:64px 0 40px;
      animation: fadeIn .8s ease-out;
    }
    
    .section-title{ 
      margin:0 0 12px; 
      font-size:clamp(32px,4vw,42px); 
      font-weight:900; 
      letter-spacing:-.02em;
      background: linear-gradient(135deg, var(--text) 0%, var(--accent) 100%);
      -webkit-background-clip:text;
      -webkit-text-fill-color:transparent;
      background-clip:text;
    }
    
    .section-sub{ 
      margin:0; 
      color:var(--text-muted); 
      font-size:1.15rem;
    }
    
    /* Feature Grid */
    .feature-grid{ 
      display:grid; 
      gap:24px; 
      grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));
      margin-bottom:64px;
    }
    
    .feature-card{
      position:relative;
      background: rgba(255,255,255,.7);
      backdrop-filter: blur(10px);
      border:1px solid var(--glass-border);
      border-radius:24px; 
      padding:32px 28px;
      transition: all .4s cubic-bezier(.4,0,.2,1);
      cursor:pointer;
    }
    
    .feature-card::before{
      content:''; position:absolute; inset:0;
      border-radius:24px; padding:1px;
      background: linear-gradient(135deg, var(--accent), transparent);
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      opacity:0; transition:opacity .4s;
    }
    
    .feature-card:hover{
      transform:translateY(-8px);
      background: rgba(255,255,255,.9);
      box-shadow: 0 20px 60px rgba(139,191,252,.2), 0 0 0 1px var(--accent);
    }
    
    .feature-card:hover::before{ opacity:1; }
    
    .feature-icon{
      font-size:2.5rem; 
      margin-bottom:16px;
      filter: drop-shadow(0 4px 12px var(--accent-glow));
    }
    
    .feature-card h3{ 
      margin:0 0 10px; 
      color:var(--text); 
      font-weight:700;
      font-size:1.25rem;
    }
    
    .feature-card p{ 
      margin:0; 
      color:var(--text-muted); 
      line-height:1.6;
    }
    
    /* Action Cards */
    .action-grid{
      display:grid;
      gap:28px;
      grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));
      margin-bottom:48px;
    }
    
    .action-card{
      position:relative; overflow:hidden;
      background: rgba(255,255,255,.6);
      backdrop-filter: blur(10px);
      border:1px solid var(--glass-border);
      border-radius:28px;
      padding:40px 36px;
      transition: all .4s cubic-bezier(.4,0,.2,1);
    }
    
    .action-card::after{
      content:''; position:absolute; top:0; right:0;
      width:200px; height:200px; border-radius:50%;
      background: radial-gradient(circle, rgba(139,191,252,.2) 0%, transparent 70%);
      transform:translate(50%, -50%);
      transition:transform .4s;
    }
    
    .action-card:hover{
      transform:translateY(-6px);
      background: rgba(255,255,255,.8);
      box-shadow: 0 25px 70px rgba(139,191,252,.25);
      border-color:var(--accent);
    }
    
    .action-card:hover::after{
      transform:translate(40%, -40%) scale(1.2);
    }
    
    .action-content{ position:relative; z-index:1; }
    
    .action-card h4{
      margin:0 0 12px;
      font-size:1.5rem;
      font-weight:700;
      color:var(--text);
    }
    
    .action-card p{
      margin:0 0 24px;
      color:var(--text-muted);
      line-height:1.6;
    }
    
    /* Streamlit Button Override */
    .stButton > button{
      width:100%;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
      color:#fff; border:0;
      padding:14px 24px;
      border-radius:14px;
      font-weight:700;
      font-size:1.05rem;
      transition: all .3s cubic-bezier(.4,0,.2,1);
      box-shadow: 0 10px 30px rgba(139,191,252,.3);
    }
    
    .stButton > button:hover{
      transform:translateY(-2px);
      box-shadow: 0 15px 40px rgba(139,191,252,.4);
      filter:brightness(1.1);
    }
    
    /* Stats Section */
    .stats-grid{
      display:grid;
      gap:20px;
      grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));
      margin:48px 0;
    }
    
    .stat-card{
      background:rgba(255,255,255,.7);
      backdrop-filter: blur(10px);
      border:1px solid var(--glass-border);
      border-radius:20px;
      padding:28px 24px;
      text-align:center;
      transition:transform .3s;
    }
    
    .stat-card:hover{ 
      transform:scale(1.05); 
      background:rgba(255,255,255,.9);
      box-shadow: 0 10px 30px rgba(139,191,252,.15);
    }
    
    .stat-number{
      font-size:2.5rem;
      font-weight:900;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
      -webkit-background-clip:text;
      -webkit-text-fill-color:transparent;
      margin-bottom:8px;
    }
    
    .stat-label{
      color:var(--text-muted);
      font-weight:600;
      text-transform:uppercase;
      font-size:.85rem;
      letter-spacing:.05em;
    }
    
    /* Footer */
    .footer{ 
      margin-top:80px; 
      padding-top:32px; 
      border-top:1px solid var(--border);
      text-align:center; 
      color:var(--text-muted);
      font-size:.95rem;
    }
    
    @media (max-width:768px){ 
      .hero{ flex-direction:column; text-align:center; padding:40px 28px; }
      .cta-group{ justify-content:center; }
      .section-header{ margin:48px 0 32px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- Hero Section ----------
  st.markdown("""
    <div class="hero" style="justify-content:center; text-align:center;">
      <div class="hero-content" style="width:100%;">
        <h1 style="font-size:clamp(40px,7vw,64px); font-weight:900; color:#fff; text-shadow:0 2px 20px rgba(0,0,0,.3); margin-bottom:10px;">🫧 SoulSolace</h1>
        <div class="tagline" style="font-size:clamp(22px,3vw,32px); font-weight:700; color:rgba(255,255,255,.95); margin-bottom:18px; text-shadow:0 1px 10px rgba(0,0,0,.2);">Empowering Minds, Enriching Lives</div>
        <p style="color:rgba(255,255,255,.90); font-size:1.25rem; line-height:1.8; max-width:700px; margin:0 auto 28px;">
Your caring companion for emotional wellness and growth.<br>
Discover a safe space to share, reflect, and heal with understanding, empathy, and personalized support.
</p>
<div style="margin-top:30px;">
          <span style="display:inline-block; width:60px; height:4px; background:linear-gradient(90deg,#8bbffc,#4a90e2); border-radius:2px;"></span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Stats ----------
  st.markdown("""
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Always Available</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Confidential</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">∞</div>
        <div class="stat-label">Possibilities</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">1</div>
        <div class="stat-label">Safe Space</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Features ----------
  st.markdown("""
    <div class="section-header" id="features">
      <h2 class="section-title">Powerful Features</h2>
      <p class="section-sub">Everything you need for your mental wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

  st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Text Chat</h3>
        <p>Empowering conversations with thoughtful, tailored and personalised support.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎙️</div>
        <h3>Voice Chat</h3>
        <p>Experience interactive voice guidance for a more personal and immersive connection.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Privacy First</h3>
        <p>Your data is secure, confidential, and always under your complete control.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🌟</div>
        <h3>Personalized</h3>
        <p>AI-powered recommendations that adapt to your unique needs and preferences.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Get Started ----------
  st.markdown("""
    <div class="section-header" id="get-started">
      <h2 class="section-title">Choose Your Path</h2>
      <p class="section-sub">Select how you'd like to begin your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

  col1, col2 = st.columns(2, gap="large")

  with col1:
        st.markdown("""
        <div class="action-card">
          <div class="action-content">
            <h4>⌨️ Text Chat</h4>
            <p>Connect through written conversation. Perfect for thoughtful, detailed discussions and resource sharing.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        # Button inside the box
        st.markdown("<div style='margin-top:-20px; text-align:center;'>", unsafe_allow_html=True)
        if st.button("Start Text Chat →", key="text_chat_box"):
          st.switch_page("pages/Text_Chat.py")
          st.markdown("</div>", unsafe_allow_html=True)

  with col2:
        st.markdown("""
        <div class="action-card">
          <div class="action-content">
            <h4>🎙️ Voice Chat</h4>
            <p>Engage through voice for a hands-free, immersive wellness experience that feels natural and personal.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:-20px; text-align:center;'>", unsafe_allow_html=True)
        if st.button("Start Voice Chat →", key="voice_chat_box"):
          st.switch_page("pages/Voice_Chat.py")
          st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Footer ----------
  st.markdown('<div class="footer">© 2025 SoulSolace — Empowering Minds, Enriching Lives<br>Your wellness journey begins here.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()