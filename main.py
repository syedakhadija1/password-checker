import streamlit as st
import re
import time
import random
import pyperclip 

# Set page config FIRST (must be the first Streamlit command)
st.set_page_config(
    page_title="Password Generator Meter",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Pink, Sky Blue, and Purple Theme Styling
st.markdown("""
    <style>
    /* General Styling */
    body { 
        background: linear-gradient(135deg, #FF9A9E, #FAD0C4, #A1C4FD, #C2E9FB);
        color: #333333; 
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
    }
    /* Animated Gradient Heading */
    .animated-heading {
        background: linear-gradient(135deg, #FF6F61, #6B5B95, #88B04B);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-animation 5s ease infinite;
        text-align: center;
    }
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.8);
        color: #333333;
        border-radius: 12px;
        border: 1px solid #DDDDDD;
        padding: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input:focus {
        border-color: #6B5B95;
        box-shadow: 0 0 0 3px rgba(107, 91, 149, 0.3);
    }
    .strength-bar {
        height: 15px;
        border-radius: 12px;
        margin: 15px 0;
        transition: width 0.5s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .weak { background-color: #FF6F61; }
    .moderate { background-color: #FFB347; }
    .strong { background-color: #88B04B; }
    .footer {
        text-align: center;
        margin-top: 30px;
        font-size: 0.9em;
        color: #6B5B95;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        border: 1px solid #DDDDDD;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .suggestions {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        border: 1px solid #DDDDDD;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .suggestions strong {
        color: #6B5B95;
    }
    .stButton>button {
        background-color: #6B5B95;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        font-size: 16px;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #4B3F72;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .toggle-password {
        color: #6B5B95;
        cursor: pointer;
        font-size: 14px;
        margin-top: 5px;
    }
    .toggle-password:hover {
        text-decoration: underline;
    }
    .copy-password {
        color: #6B5B95;
        cursor: pointer;
        font-size: 14px;
        margin-top: 5px;
    }
    .copy-password:hover {
        text-decoration: underline;
    }
    .generated-password {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #DDDDDD;
        margin-top: 15px;
        font-family: monospace;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .card {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #DDDDDD;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Function to check password strength
def check_password_meter(password):
    strength = 0
    suggestions = []

    # Length Check
    if len(password) >= 8:
        strength += 1
    else:
        suggestions.append("📏 Use at least 8 characters.")

    if len(password) >= 12:
        strength += 1

    # Uppercase Check
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        suggestions.append("🔠 Add uppercase letters (A-Z).")

    # Lowercase Check
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        suggestions.append("🔡 Add lowercase letters (a-z).")

    # Number Check
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        suggestions.append("🔢 Include numbers (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1
    else:
        suggestions.append("🔣 Use special characters (!@#$%^&*).")

    # Strength Levels
    if strength <= 2:
        remarks = "❌ Weak"
        color = "weak"
    elif strength <= 4:
        remarks = "⚠️ Moderate"
        color = "moderate"
    else:
        remarks = "✅ Strong"
        color = "strong"

    return remarks, strength, color, suggestions

# Function to generate a strong password
def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = "".join(random.choice(chars) for _ in range(16))
    return password

# Streamlit UI
st.markdown("<h1 class='animated-heading'>Password Generator Meter</h1>", unsafe_allow_html=True)

# Animated Subheading
with st.empty():
    for text in ["Type your password below...", "Ensure it's secure!", "Stay protected!"]:
        time.sleep(0.8)
        st.markdown(f"<h4 style='text-align: center; color: #6B5B95;'>{text}</h4>", unsafe_allow_html=True)

# Password input field
password = st.text_input("Enter your password:", type="password", placeholder="Type your password here...", key="password_input")

# Toggle Password Visibility
show_password = st.checkbox("👁️ Show Password")
if show_password:
    st.text_input("", value=password, type="default", key="visible_password", disabled=True)


if password:
    if st.button("📋 Copy Password to Clipboard"):
        pyperclip.copy(password)
        st.success("Password copied to clipboard!")

if st.button("🎲 Generate Strong Password"):
    generated_password = generate_password()
    st.markdown(f"<div class='generated-password'>{generated_password}</div>", unsafe_allow_html=True)
    if st.button("📋 Copy Generated Password"):
        pyperclip.copy(generated_password)
        st.success("Generated password copied to clipboard!")


if password:
    remarks, strength, color, suggestions = check_password_meter(password)

    # Display Strength
    st.markdown(f"<h3 style='color: #333333; text-align: center;'>Strength: {remarks}</h3>", unsafe_allow_html=True)

    # Animated Progress Bar
    progress_color = {"weak": "#FF6F61", "moderate": "#FFB347", "strong": "#88B04B"}
    bar_html = f"""
        <div class="strength-bar {color}" style="background-color: {progress_color[color]}; width: {strength * 16.6}%;"></div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)

    # Suggestions
    if suggestions:
        st.markdown("<div class='suggestions'>💡 <strong>Tips to improve your password:</strong></div>", unsafe_allow_html=True)
        for tip in suggestions:
            st.markdown(f"<div class='suggestions'>• {tip}</div>", unsafe_allow_html=True)
    else:
        st.success("🎉 Your password is strong and secure!")

# Footer
st.markdown("---")
st.markdown("""
    <div class='footer'>
        🔒 Developed with ❤️ Syeda Khadija Abrar | Stay Secure! 🚀<br>
      
    </div>
""", unsafe_allow_html=True)