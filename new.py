import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json
import datetime
import random
import time
from googletrans import Translator
import sqlite3
from textblob import TextBlob
import base64sssss  
import threading
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment
import speech_recognition as sr
from collections import defaultdict
import re
import langdetect
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import requests
from functools import lru_cache
import concurrent.futures
import unicodedata

# Page configuration
st.set_page_config(
    page_title="NeuroLink Universal Translator 3.0",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_app_state():
    """Initialize comprehensive session state for universal language support"""
    defaults = {
        'universal_vocabulary_bank': [],
        'conversation_history': [],
        'language_detection_history': [],
        'multilingual_cache': {},
        'learning_streak': 0,
        'user_level': 1,
        'daily_words_learned': 0,
        'total_experience_points': 0,
        'user_mood': 'motivated',
        'learning_preferences': 'audio_visual',
        'ai_teacher_mode': 'high IQ',
        'primary_language': 'en',
        'target_languages': ['es', 'fr', 'de'],
        'learning_session_active': False,
        'favorite_words': [],
        'achievement_badges': [],
        'study_time_today': 0,
        'pronunciation_practice_count': 0,
        'audio_enabled': True,
        'speech_speed': 'normal',
        'pronunciation_score_history': [],
        'audio_cache': {},
        'voice_preference': 'auto',
        'pronunciation_difficulty': 'intermediate',
        'listening_comprehension_score': 0,
        'audio_exercises_completed': 0,
        'speech_recognition_accuracy': 0.0,
        'audio_learning_streak': 0,
        'universal_translation_mode': True,
        'auto_detect_language': True,
        'supported_languages_count': 0,
        'translation_confidence_threshold': 0.7
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_app_state()

# Enhanced styling with universal language support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .universal-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #ffecd2 100%);
        padding: 4rem 2rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .universal-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .language-detection-card {
        background: linear-gradient(135deg, #00c9ff, #92fe9d);
        color: white;
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 201, 255, 0.3);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .language-detection-card::after {
        content: '🌐';
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.3;
    }
    
    .universal-translation-result {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
        border: 3px solid #00ff88;
        border-radius: 25px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0, 255, 136, 0.2);
        position: relative;
    }
    
    .universal-translation-result::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        border-radius: 25px 25px 0 0;
    }
    
    .multilingual-chip {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 30px;
        margin: 0.5rem;
        display: inline-block;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .multilingual-chip::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .multilingual-chip:hover::before {
        left: 100%;
    }
    
    .multilingual-chip:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    .language-confidence-meter {
        background: linear-gradient(90deg, #ff4757 0%, #ffa502 50%, #2ed573 100%);
        height: 25px;
        border-radius: 15px;
        position: relative;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .confidence-indicator {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .universal-audio-controls {
        display: flex;
        gap: 1rem;
        align-items: center;
        justify-content: center;
        margin: 1.5rem 0;
        flex-wrap: wrap;
        padding: 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .premium-audio-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.4s ease;
        font-weight: 600;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .premium-audio-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .premium-audio-button:hover::before {
        left: 100%;
    }
    
    .premium-audio-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
    }
    
    .premium-audio-button:active {
        transform: translateY(-1px) scale(0.98);
    }
    
    .sentence-analysis-card {
        background: linear-gradient(135deg, #ff9a9e, #fecfef);
        color: #333;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(255, 154, 158, 0.3);
    }
    
    .word-breakdown {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .word-item {
        background: rgba(255,255,255,0.9);
        padding: 0.8rem 1.2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .word-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .language-family-badge {
        background: linear-gradient(45deg, #ffecd2, #fcb69f);
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .universal-stats-dashboard {
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        color: white;
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .universal-stats-dashboard::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .realtime-translation-input {
        background: rgba(255,255,255,0.95);
        border: 3px solid #667eea;
        border-radius: 25px;
        padding: 1.5rem 2rem;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .realtime-translation-input:focus {
        border-color: #f093fb;
        box-shadow: 0 0 0 3px rgba(240, 147, 251, 0.2);
        outline: none;
    }
    
    .language-detection-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(0, 255, 136, 0.1);
        color: #00aa5a;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .multilingual-conversation {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        margin: 1rem 0;
    }
    
    .conversation-message {
        margin: 1rem 0;
        padding: 1.5rem;
        border-radius: 20px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .message-original {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: 0;
        border-radius: 20px 20px 20px 5px;
    }
    
    .message-translated {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #333;
        margin-left: auto;
        border-radius: 20px 20px 5px 20px;
    }
    
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 1rem;
    }
    
    .typing-dot {
        width: 10px;
        height: 10px;
        background: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(2) { animation-delay: -0.32s; }
    .typing-dot:nth-child(3) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

class UniversalLanguageDatabase:
    """Comprehensive database for all world languages with advanced features"""
    
    def __init__(self):
        self.supported_languages = self.initialize_comprehensive_language_support()
        self.language_families = self.initialize_language_families()
        self.cultural_contexts = self.initialize_cultural_contexts()
        self.phonetic_systems = self.initialize_phonetic_systems()
        
    def initialize_comprehensive_language_support(self):
        """Initialize support for 100+ languages with detailed metadata"""
        return {
            # Major World Languages
            'en': {'name': 'English', 'flag': '🇺🇸', 'family': 'Germanic', 'script': 'Latin', 'speakers': 1500000000, 'difficulty': 1},
            'zh': {'name': 'Chinese (Mandarin)', 'flag': '🇨🇳', 'family': 'Sino-Tibetan', 'script': 'Chinese', 'speakers': 918000000, 'difficulty': 5},
            'hi': {'name': 'Hindi', 'flag': '🇮🇳', 'family': 'Indo-European', 'script': 'Devanagari', 'speakers': 602000000, 'difficulty': 4},
            'es': {'name': 'Spanish', 'flag': '🇪🇸', 'family': 'Romance', 'script': 'Latin', 'speakers': 559000000, 'difficulty': 2},
            'fr': {'name': 'French', 'flag': '🇫🇷', 'family': 'Romance', 'script': 'Latin', 'speakers': 280000000, 'difficulty': 3},
            'ar': {'name': 'Arabic', 'flag': '🇸🇦', 'family': 'Semitic', 'script': 'Arabic', 'speakers': 422000000, 'difficulty': 5},
            'bn': {'name': 'Bengali', 'flag': '🇧🇩', 'family': 'Indo-European', 'script': 'Bengali', 'speakers': 300000000, 'difficulty': 4},
            'pt': {'name': 'Portuguese', 'flag': '🇵🇹', 'family': 'Romance', 'script': 'Latin', 'speakers': 270000000, 'difficulty': 2},
            'ru': {'name': 'Russian', 'flag': '🇷🇺', 'family': 'Slavic', 'script': 'Cyrillic', 'speakers': 258000000, 'difficulty': 4},
            'ja': {'name': 'Japanese', 'flag': '🇯🇵', 'family': 'Japonic', 'script': 'Hiragana/Katakana/Kanji', 'speakers': 125000000, 'difficulty': 5},
            'pa': {'name': 'Punjabi', 'flag': '🇮🇳', 'family': 'Indo-European', 'script': 'Gurmukhi', 'speakers': 113000000, 'difficulty': 3},
            'de': {'name': 'German', 'flag': '🇩🇪', 'family': 'Germanic', 'script': 'Latin', 'speakers': 100000000, 'difficulty': 3},
            'jv': {'name': 'Japanese', 'flag': '🇮🇩', 'family': 'Austronesian', 'script': 'Latin/Japanese', 'speakers': 82000000, 'difficulty': 3},
            'ko': {'name': 'Korean', 'flag': '🇰🇷', 'family': 'Koreanic', 'script': 'Hangul', 'speakers': 81000000, 'difficulty': 4},
            'te': {'name': 'Telugu', 'flag': '🇮🇳', 'family': 'Dravidian', 'script': 'Telugu', 'speakers': 75000000, 'difficulty': 4},
            
            # European Languages
            'it': {'name': 'Italian', 'flag': '🇮🇹', 'family': 'Romance', 'script': 'Latin', 'speakers': 65000000, 'difficulty': 2},
            'tr': {'name': 'Turkish', 'flag': '🇹🇷', 'family': 'Turkic', 'script': 'Latin', 'speakers': 88000000, 'difficulty': 4},
            'pl': {'name': 'Polish', 'flag': '🇵🇱', 'family': 'Slavic', 'script': 'Latin', 'speakers': 45000000, 'difficulty': 4},
            'uk': {'name': 'Ukrainian', 'flag': '🇺🇦', 'family': 'Slavic', 'script': 'Cyrillic', 'speakers': 40000000, 'difficulty': 4},
            'nl': {'name': 'Dutch', 'flag': '🇳🇱', 'family': 'Germanic', 'script': 'Latin', 'speakers': 25000000, 'difficulty': 2},
            'el': {'name': 'Greek', 'flag': '🇬🇷', 'family': 'Indo-European', 'script': 'Greek', 'speakers': 13000000, 'difficulty': 4},
            'cs': {'name': 'Czech', 'flag': '🇨🇿', 'family': 'Slavic', 'script': 'Latin', 'speakers': 10000000, 'difficulty': 4},
            'sv': {'name': 'Swedish', 'flag': '🇸🇪', 'family': 'Germanic', 'script': 'Latin', 'speakers': 10000000, 'difficulty': 2},
            'he': {'name': 'Hebrew', 'flag': '🇮🇱', 'family': 'Semitic', 'script': 'Hebrew', 'speakers': 9000000, 'difficulty': 5},
            'no': {'name': 'Norwegian', 'flag': '🇳🇴', 'family': 'Germanic', 'script': 'Latin', 'speakers': 5000000, 'difficulty': 2},
            'da': {'name': 'Danish', 'flag': '🇩🇰', 'family': 'Germanic', 'script': 'Latin', 'speakers': 6000000, 'difficulty': 2},
            'fi': {'name': 'Finnish', 'flag': '🇫🇮', 'family': 'Uralic', 'script': 'Latin', 'speakers': 5000000, 'difficulty': 5},
            'hu': {'name': 'Hungarian', 'flag': '🇭🇺', 'family': 'Uralic', 'script': 'Latin', 'speakers': 13000000, 'difficulty': 5},
            
            # African Languages
            'sw': {'name': 'Swahili', 'flag': '🇹🇿', 'family': 'Niger-Congo', 'script': 'Latin', 'speakers': 200000000, 'difficulty': 3},
            'am': {'name': 'Amharic', 'flag': '🇪🇹', 'family': 'Semitic', 'script': 'Ethiopic', 'speakers': 57000000, 'difficulty': 4},
            'yo': {'name': 'Yoruba', 'flag': '🇳🇬', 'family': 'Niger-Congo', 'script': 'yoruba', 'speakers': 45000000, 'difficulty': 3},
            'zu': {'name': 'Zulu', 'flag': '🇿🇦', 'family': 'Niger-Congo', 'script': 'Latin', 'speakers': 27000000, 'difficulty': 4},
            'ig': {'name': 'Igbo', 'flag': '🇳🇬', 'family': 'Niger-Congo', 'script': 'igbo', 'speakers': 27000000, 'difficulty': 3},
            'ha': {'name': 'Hausa', 'flag': '🇳🇬', 'family': 'Afroasiatic', 'script': 'hausa', 'speakers': 70000000, 'difficulty': 3},
            
            # Asian Languages
            'th': {'name': 'Thai', 'flag': '🇹🇭', 'family': 'Kra-Dai', 'script': 'Thai', 'speakers': 69000000, 'difficulty': 5},
            'vi': {'name': 'Vietnamese', 'flag': '🇻🇳', 'family': 'Austroasiatic', 'script': 'Latin', 'speakers': 95000000, 'difficulty': 4},
            'ta': {'name': 'Tamil', 'flag': '🇮🇳', 'family': 'Dravidian', 'script': 'Tamil', 'speakers': 78000000, 'difficulty': 4},
            'ur': {'name': 'Urdu', 'flag': '🇵🇰', 'family': 'Indo-European', 'script': 'Arabic', 'speakers': 232000000, 'difficulty': 4},
            'ml': {'name': 'Malayalam', 'flag': '🇮🇳', 'family': 'Dravidian', 'script': 'Malayalam', 'speakers': 38000000, 'difficulty': 4},
            'kn': {'name': 'Kannada', 'flag': '🇮🇳', 'family': 'Dravidian', 'script': 'Kannada', 'speakers': 44000000, 'difficulty': 4},
            'gu': {'name': 'Gujarati', 'flag': '🇮🇳', 'family': 'Indo-European', 'script': 'Gujarati', 'speakers': 56000000, 'difficulty': 4},
            'or': {'name': 'Odia', 'flag': '🇮🇳', 'family': 'Indo-European', 'script': 'Odia', 'speakers': 38000000, 'difficulty': 4},
            'my': {'name': 'Burmese', 'flag': '🇲🇲', 'family': 'Sino-Tibetan', 'script': 'Myanmar', 'speakers': 33000000, 'difficulty': 5},
            'km': {'name': 'Khmer', 'flag': '🇰🇭', 'family': 'Austroasiatic', 'script': 'Khmer', 'speakers': 16000000, 'difficulty': 5},
            'lo': {'name': 'Lao', 'flag': '🇱🇦', 'family': 'Kra-Dai', 'script': 'Lao', 'speakers': 30000000, 'difficulty': 4},
            
            # Additional Languages
            'id': {'name': 'Indonesian', 'flag': '🇮🇩', 'family': 'Austronesian', 'script': 'Latin', 'speakers': 270000000, 'difficulty': 2},
            'ms': {'name': 'Malay', 'flag': '🇲🇾', 'family': 'Austronesian', 'script': 'Latin', 'speakers': 290000000, 'difficulty': 2},
            'tl': {'name': 'Filipino', 'flag': '🇵🇭', 'family': 'Austronesian', 'script': 'Latin', 'speakers': 45000000, 'difficulty': 2},
            'ne': {'name': 'Nepali', 'flag': '🇳🇵', 'family': 'Indo-European', 'script': 'Devanagari', 'speakers': 16000000, 'difficulty': 4},
            'si': {'name': 'Sinhala', 'flag': '🇱🇰', 'family': 'Indo-European', 'script': 'Sinhala', 'speakers': 17000000, 'difficulty': 4},
            'mn': {'name': 'Mongolian', 'flag': '🇲🇳', 'family': 'Mongolic', 'script': 'Cyrillic/Mongolian', 'speakers': 5000000, 'difficulty': 4},
            'ka': {'name': 'Georgian', 'flag': '🇬🇪', 'family': 'Kartvelian', 'script': 'Georgian', 'speakers': 4000000, 'difficulty': 5},
            'hy': {'name': 'Armenian', 'flag': '🇦🇲', 'family': 'Indo-European', 'script': 'Armenian', 'speakers': 7000000, 'difficulty': 4},
            'az': {'name': 'Azerbaijani', 'flag': '🇦🇿', 'family': 'Turkic', 'script': 'Latin', 'speakers': 23000000, 'difficulty': 3},
            'kk': {'name': 'Kazakh', 'flag': '🇰🇿', 'family': 'Turkic', 'script': 'Cyrillic', 'speakers': 13000000, 'difficulty': 4},
            'ky': {'name': 'Kyrgyz', 'flag': '🇰🇬', 'family': 'Turkic', 'script': 'Cyrillic', 'speakers': 5000000, 'difficulty': 4},
            'uz': {'name': 'Uzbek', 'flag': '🇺🇿', 'family': 'Turkic', 'script': 'Latin', 'speakers': 34000000, 'difficulty': 3},
            'fa': {'name': 'Persian', 'flag': '🇮🇷', 'family': 'Indo-European', 'script': 'Arabic', 'speakers': 70000000, 'difficulty': 4},
            'ps': {'name': 'Pashto', 'flag': '🇦🇫', 'family': 'Indo-European', 'script': 'Arabic', 'speakers': 60000000, 'difficulty': 4},
        }
    
    def initialize_language_families(self):
        """Detailed language family classifications"""
        return {
            'Indo-European': {
                'sub_families': ['Germanic', 'Romance', 'Slavic', 'Indo-Iranian'],
                'characteristics': 'Largest language family, includes most European languages',
                'origin': 'Proto-Indo-European (c. 3500-2500 BCE)'
            },
            'Sino-Tibetan': {
                'sub_families': ['Chinese', 'Tibeto-Burman'],
                'characteristics': 'Tonal languages, logographic writing systems',
                'origin': 'Ancient China and Tibet region'
            },
            'Afroasiatic': {
                'sub_families': ['Semitic', 'Egyptian', 'Berber', 'Cushitic', 'Chadic'],
                'characteristics': 'Root-and-pattern morphology, pharyngeal sounds',
                'origin': 'Northeast Africa'
            },
            'Niger-Congo': {
                'sub_families': ['Bantu', 'West Atlantic', 'Mande'],
                'characteristics': 'Noun class systems, rich tonal systems',
                'origin': 'Sub-Saharan Africa'
            },
            'Austronesian': {
                'sub_families': ['Malayo-Polynesian', 'Formosan'],
                'characteristics': 'Maritime dispersal, verb-initial word order',
                'origin': 'Taiwan and Southeast Asia'
            }
        }
    
    def initialize_cultural_contexts(self):
        """Cultural and contextual information for languages"""
        return {
            'greetings': {
                'formal': {'en': 'Good morning/afternoon/evening', 'es': 'Buenos días/tardes/noches', 'fr': 'Bonjour/Bonsoir', 'de': 'Guten Tag/Abend', 'ja': 'おはようございます/こんにちは', 'ar': 'السلام عليكم', 'zh': '您好', 'hi': 'नमस्ते'},
                'casual': {'en': 'Hi/Hello', 'es': 'Hola', 'fr': 'Salut', 'de': 'Hallo', 'ja': 'こんにちは', 'ar': 'أهلا', 'zh': '你好', 'hi': 'नमस्कार'}
            },
            'politeness_markers': {
                'please': {'en': 'please', 'es': 'por favor', 'fr': 's\'il vous plaît', 'de': 'bitte', 'ja': 'お願いします', 'ar': 'من فضلك', 'zh': '请', 'hi': 'कृपया'},
                'thank_you': {'en': 'thank you', 'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'ja': 'ありがとう', 'ar': 'شكرا', 'zh': '谢谢', 'hi': 'धन्यवाद'}
            },
            'cultural_notes': {
                'es': 'Spanish varies significantly across regions. Mexican Spanish differs from Argentinian Spanish.',
                'ja': 'Japanese has complex honorific systems (keigo) that vary based on social relationships.',
                'ar': 'Arabic has numerous dialects; Modern Standard Arabic is used in formal contexts.',
                'zh': 'Mandarin Chinese uses four main tones that completely change word meanings.',
                'hi': 'Hindi shares vocabulary with Urdu but uses different scripts (Devanagari vs Arabic).',
                'fr': 'French pronunciation varies between regions; liaison rules affect speech patterns.',
                'de': 'German has three grammatical genders and four cases affecting article usage.',
                'ru': 'Russian uses six grammatical cases and has no articles (a, an, the).',
                'ko': 'Korean has multiple speech levels based on age, status, and relationship formality.',
                'th': 'Thai has five tones and no spaces between words in traditional writing.'
            }
        }
    
    def initialize_phonetic_systems(self):
        """Phonetic guides and pronunciation systems"""
        return {
            'ipa_support': True,
            'romanization_systems': {
                'zh': 'Pinyin', 'ja': 'Romaji', 'ko': 'Revised Romanization', 
                'ar': 'DIN 31635', 'ru': 'BGN/PCGN', 'hi': 'IAST', 'th': 'Royal Thai'
            },
            'tone_languages': ['zh', 'th', 'vi', 'my', 'lo'],
            'stress_patterns': {
                'es': 'penultimate_stress', 'fr': 'final_stress', 'en': 'variable_stress',
                'de': 'initial_stress', 'ru': 'variable_stress', 'it': 'penultimate_stress'
            }
        }

class AdvancedAudioManager:
    """Enhanced audio management with universal language support"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.recognizer = sr.Recognizer()
        self.language_db = UniversalLanguageDatabase()
        
        # Enhanced TTS configurations for all supported languages
        self.tts_configs = self.initialize_comprehensive_tts_configs()
        
        # Advanced speed and quality settings
        self.speed_settings = {
            'very_slow': {'slow': True, 'speed_multiplier': 0.5},
            'slow': {'slow': True, 'speed_multiplier': 0.7},
            'normal': {'slow': False, 'speed_multiplier': 1.0},
            'fast': {'slow': False, 'speed_multiplier': 1.3},
            'very_fast': {'slow': False, 'speed_multiplier': 1.6}
        }
        
        # Voice quality settings
        self.voice_qualities = {
            'standard': {'lang_tld_mapping': 'default'},
            'premium': {'lang_tld_mapping': 'enhanced'},
            'native': {'lang_tld_mapping': 'native_region'}
        }
    
    def initialize_comprehensive_tts_configs(self):
        """Initialize TTS configurations for all supported languages"""
        configs = {}
        for lang_code, lang_info in self.language_db.supported_languages.items():
            configs[lang_code] = {
                'tld': self.get_optimal_tld(lang_code, lang_info),
                'slow': False,
                'supports_ssml': lang_code in ['en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'ko'],
                'voice_variants': self.get_voice_variants(lang_code)
            }
        return configs
    
    def get_optimal_tld(self, lang_code, lang_info):
        """Get optimal TLD for each language for best pronunciation"""
        tld_mapping = {
            'en': 'com', 'es': 'es', 'fr': 'fr', 'de': 'de', 'it': 'it', 'pt': 'com.br',
            'ja': 'co.jp', 'ko': 'co.kr', 'zh': 'com', 'ru': 'ru', 'ar': 'com',
            'hi': 'co.in', 'nl': 'nl', 'tr': 'com.tr', 'pl': 'pl', 'uk': 'com.ua',
            'el': 'gr', 'cs': 'cz', 'sv': 'se', 'he': 'com', 'no': 'no', 'da': 'dk',
            'fi': 'fi', 'hu': 'hu', 'th': 'co.th', 'vi': 'com.vn', 'id': 'co.id',
            'ms': 'com.my', 'tl': 'com.ph', 'sw': 'co.ke', 'am': 'com', 'yo': 'com',
            'zu': 'co.za', 'ig': 'com', 'ha': 'com', 'ta': 'co.in', 'ur': 'com.pk',
            'ml': 'co.in', 'kn': 'co.in', 'gu': 'co.in', 'or': 'co.in', 'my': 'com',
            'km': 'com', 'lo': 'com', 'ne': 'com', 'si': 'lk', 'mn': 'mn',
            'ka': 'ge', 'hy': 'am', 'az': 'az', 'kk': 'kz', 'ky': 'kg',
            'uz': 'uz', 'fa': 'com', 'ps': 'com'
        }
        return tld_mapping.get(lang_code, 'com')
    
    def get_voice_variants(self, lang_code):
        """Get available voice variants for each language"""
        variants = {
            'en': ['us', 'uk', 'au', 'ca', 'in'],
            'es': ['es', 'mx', 'ar', 'co', 'cl'],
            'fr': ['fr', 'ca', 'ch'],
            'de': ['de', 'at', 'ch'],
            'pt': ['br', 'pt'],
            'ar': ['sa', 'eg', 'ae', 'ma'],
            'zh': ['cn', 'tw', 'hk'],
        }
        return variants.get(lang_code, ['default'])
    
    def generate_universal_tts(self, text, language, speed='normal', voice_variant='default'):
        """Generate TTS for any supported language with advanced options"""
        try:
            # Language detection if auto-detect is enabled
            if st.session_state.auto_detect_language and language == 'auto':
                language = self.detect_language(text)
            
            # Get language configuration
            config = self.tts_configs.get(language, {'tld': 'com', 'slow': False})
            speed_config = self.speed_settings.get(speed, self.speed_settings['normal'])
            
            # Create comprehensive cache key
            cache_key = f"{text[:50]}_{language}_{speed}_{voice_variant}_{hash(text)}"
            
            # Check cache first
            if cache_key in st.session_state.audio_cache:
                return st.session_state.audio_cache[cache_key]
            
            # Handle long texts by breaking them into chunks
            if len(text) > 5000:  # gTTS limit
                return self.generate_long_text_tts(text, language, speed, voice_variant)
            
            # Generate TTS with enhanced parameters
            tts = gTTS(
                text=text,
                lang=language,
                slow=speed_config.get('slow', config['slow']),
                tld=config['tld']
            )
            
            # Save to temporary file with unique naming
            temp_file = os.path.join(self.temp_dir, f"tts_{cache_key.replace(' ', '_')[:100]}.mp3")
            tts.save(temp_file)
            
            # Apply advanced audio processing
            if speed_config['speed_multiplier'] != 1.0:
                temp_file = self.modify_audio_speed(temp_file, speed_config['speed_multiplier'])
            
            # Cache the result
            st.session_state.audio_cache[cache_key] = temp_file
            
            return temp_file
            
        except Exception as e:
            st.error(f"TTS Generation Error for {language}: {e}")
            return None
    
    def generate_long_text_tts(self, text, language, speed, voice_variant):
        """Handle long texts by chunking and concatenating audio"""
        try:
            # Split text into manageable chunks
            chunks = self.smart_text_chunking(text, max_length=4000)
            audio_files = []
            
            for i, chunk in enumerate(chunks):
                chunk_file = self.generate_universal_tts(chunk, language, speed, voice_variant)
                if chunk_file:
                    audio_files.append(chunk_file)
            
            # Concatenate audio files
            if audio_files:
                return self.concatenate_audio_files(audio_files)
            
        except Exception as e:
            st.error(f"Long text TTS error: {e}")
            return None
    
    def smart_text_chunking(self, text, max_length=4000):
        """Intelligently chunk text at sentence boundaries"""
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if chunk.strip()]
    
    def concatenate_audio_files(self, audio_files):
        """Concatenate multiple audio files into one"""
        try:
            combined = AudioSegment.empty()
            
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    segment = AudioSegment.from_mp3(audio_file)
                    combined += segment
                    combined += AudioSegment.silent(duration=300)  # 300ms pause
            
            # Save combined audio
            combined_file = os.path.join(self.temp_dir, f"combined_{int(time.time())}.mp3")
            combined.export(combined_file, format="mp3")
            
            return combined_file
            
        except Exception as e:
            st.error(f"Audio concatenation error: {e}")
            return None
    
    def detect_language(self, text):
        """Detect language of input text"""
        try:
            detected_lang = detect(text)
            # Verify it's in our supported languages
            if detected_lang in self.language_db.supported_languages:
                return detected_lang
            else:
                # Return most likely supported language based on script
                return self.fallback_language_detection(text)
        except LangDetectError:
            return self.fallback_language_detection(text)
    
    def fallback_language_detection(self, text):
        """Fallback language detection based on character analysis"""
        # Analyze character sets to determine likely language
        char_analysis = {
            'latin': 0, 'cyrillic': 0, 'arabic': 0, 'chinese': 0,
            'japanese': 0, 'korean': 0, 'devanagari': 0, 'thai': 0
        }
        
        for char in text:
            code_point = ord(char)
            if 0x0000 <= code_point <= 0x007F:  # Basic Latin
                char_analysis['latin'] += 1
            elif 0x0400 <= code_point <= 0x04FF:  # Cyrillic
                char_analysis['cyrillic'] += 1
            elif 0x0600 <= code_point <= 0x06FF:  # Arabic
                char_analysis['arabic'] += 1
            elif 0x4E00 <= code_point <= 0x9FFF:  # Chinese
                char_analysis['chinese'] += 1
            elif 0x3040 <= code_point <= 0x309F or 0x30A0 <= code_point <= 0x30FF:  # Japanese
                char_analysis['japanese'] += 1
            elif 0xAC00 <= code_point <= 0xD7AF:  # Korean
                char_analysis['korean'] += 1
            elif 0x0900 <= code_point <= 0x097F:  # Devanagari (Hindi)
                char_analysis['devanagari'] += 1
            elif 0x0E00 <= code_point <= 0x0E7F:  # Thai
                char_analysis['thai'] += 1
        
        # Determine most likely script
        dominant_script = max(char_analysis, key=char_analysis.get)
        
        # Map script to language code
        script_to_lang = {
            'latin': 'en', 'cyrillic': 'ru', 'arabic': 'ar', 'chinese': 'zh',
            'japanese': 'ja', 'korean': 'ko', 'devanagari': 'hi', 'thai': 'th'
        }
        
        return script_to_lang.get(dominant_script, 'en')
    
    def modify_audio_speed(self, audio_file, speed_multiplier):
        """Advanced audio speed modification preserving quality"""
        try:
            audio = AudioSegment.from_mp3(audio_file)
            
            # Use different methods based on speed change
            if 0.7 <= speed_multiplier <= 1.3:
                # Small changes: simple rate adjustment
                new_sample_rate = int(audio.frame_rate * speed_multiplier)
                modified_audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": new_sample_rate
                }).set_frame_rate(audio.frame_rate)
            else:
                # Large changes: more sophisticated processing
                modified_audio = audio.speedup(playback_speed=speed_multiplier)
            
            # Save modified audio
            modified_file = audio_file.replace('.mp3', f'_speed_{speed_multiplier}.mp3')
            modified_audio.export(modified_file, format="mp3")
            
            return modified_file
            
        except Exception as e:
            st.error(f"Speed modification error: {e}")
            return audio_file
    
    def play_audio_streamlit(self, audio_file, autoplay=True):
        """Enhanced audio player with controls"""
        if audio_file and os.path.exists(audio_file):
            with open(audio_file, 'rb') as audio_data:
                audio_bytes = audio_data.read()
                audio_b64 = base64.b64encode(audio_bytes).decode()
                
                autoplay_attr = "autoplay" if autoplay else ""
                
                audio_html = f"""
                <div style="margin: 1rem 0;">
                    <audio controls {autoplay_attr} style="width: 100%; margin: 0.5rem 0;">
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
                return True
        return False
    
    def analyze_pronunciation_universal(self, recorded_file, target_text, target_language):
        """Advanced pronunciation analysis for any language"""
        try:
            # Use language-specific recognition
            with sr.AudioFile(recorded_file) as source:
                audio = self.recognizer.record(source)
            
            # Attempt recognition in target language
            try:
                recognized_text = self.recognizer.recognize_google(audio, language=target_language)
            except:
                # Fallback to English recognition
                recognized_text = self.recognizer.recognize_google(audio)
            
            # Advanced similarity analysis
            similarity_scores = self.calculate_advanced_similarity(target_text, recognized_text, target_language)
            
            # Generate detailed feedback
            feedback = self.generate_comprehensive_pronunciation_feedback(similarity_scores, target_language)
            
            return {
                'overall_score': similarity_scores['overall'],
                'phonetic_score': similarity_scores['phonetic'],
                'rhythm_score': similarity_scores['rhythm'],
                'recognized_text': recognized_text,
                'target_text': target_text,
                'language': target_language,
                'feedback': feedback,
                'improvement_tips': self.get_improvement_tips(similarity_scores, target_language)
            }
            
        except Exception as e:
            return {
                'overall_score': 0,
                'phonetic_score': 0,
                'rhythm_score': 0,
                'recognized_text': "Recognition failed",
                'target_text': target_text,
                'language': target_language,
                'feedback': f"Recognition error: {e}",
                'improvement_tips': ["Try speaking more clearly", "Check microphone settings"]
            }
    
    def calculate_advanced_similarity(self, target, recognized, language):
        """Calculate multiple similarity metrics"""
        from difflib import SequenceMatcher
        
        # Basic similarity
        basic_similarity = SequenceMatcher(None, target.lower(), recognized.lower()).ratio()
        
        # Phonetic similarity (simplified)
        phonetic_similarity = self.calculate_phonetic_similarity(target, recognized, language)
        
        # Length-adjusted similarity
        length_penalty = min(len(recognized), len(target)) / max(len(recognized), len(target))
        
        # Word-level similarity
        target_words = target.lower().split()
        recognized_words = recognized.lower().split()
        word_similarity = len(set(target_words) & set(recognized_words)) / max(len(target_words), len(recognized_words)) if target_words else 0
        
        return {
            'overall': int((basic_similarity * 0.4 + phonetic_similarity * 0.3 + word_similarity * 0.3) * 100),
            'phonetic': int(phonetic_similarity * 100),
            'rhythm': int(length_penalty * 100),
            'word_accuracy': int(word_similarity * 100)
        }
    
    def calculate_phonetic_similarity(self, target, recognized, language):
        """Calculate phonetic similarity based on language characteristics"""
        # Simplified phonetic similarity - would use proper phonetic analysis in production
        
        # Remove common phonetic confusions based on language
        phonetic_mappings = {
            'en': {'v': 'w', 'th': 't', 'r': 'l'},
            'es': {'b': 'v', 'r': 'rr'},
            'ja': {'r': 'l', 'f': 'h'},
            'zh': {'r': 'l', 'n': 'l'},
            'ar': {'p': 'b', 'v': 'f'}
        }
        
        # Apply language-specific mappings
        if language in phonetic_mappings:
            for original, substitute in phonetic_mappings[language].items():
                target = target.replace(original, substitute)
                recognized = recognized.replace(original, substitute)
        
        return SequenceMatcher(None, target.lower(), recognized.lower()).ratio()
    
    def generate_comprehensive_pronunciation_feedback(self, scores, language):
        """Generate detailed, language-specific feedback"""
        overall = scores['overall']
        lang_name = self.language_db.supported_languages.get(language, {}).get('name', language)
        
        if overall >= 90:
            return f"🎉 Excellent {lang_name} pronunciation! You sound almost native!"
        elif overall >= 80:
            return f"👏 Great {lang_name} pronunciation! Very clear and accurate."
        elif overall >= 70:
            return f"👍 Good {lang_name} pronunciation! Minor improvements needed."
        elif overall >= 60:
            return f"🎯 Decent {lang_name} pronunciation! Focus on clarity."
        elif overall >= 40:
            return f"📚 Keep practicing your {lang_name}! You're making progress."
        else:
            return f"💪 Don't give up on {lang_name}! Practice makes perfect."
    
    def get_improvement_tips(self, scores, language):
        """Get language-specific improvement tips"""
        tips = []
        
        lang_info = self.language_db.supported_languages.get(language, {})
        difficulty = lang_info.get('difficulty', 1)
        
        if scores['overall'] < 70:
            tips.append("Practice with native speaker recordings")
            tips.append("Break down words into syllables")
        
        if scores['phonetic'] < 60:
            tips.append(f"Focus on {lang_info.get('name', language)}-specific sounds")
            tips.append("Use pronunciation guides and phonetic transcriptions")
        
        if scores['rhythm'] < 70:
            tips.append("Pay attention to word stress and rhythm patterns")
            tips.append("Practice with longer phrases and sentences")
        
        # Language-specific tips
        language_tips = {
            'zh': ["Focus on the four tones", "Practice tone pairs"],
            'ja': ["Work on pitch accent", "Practice long and short vowels"],
            'ar': ["Focus on pharyngeal and uvular sounds", "Practice emphatic consonants"],
            'th': ["Master the five tones", "Practice retroflex consonants"],
            'fr': ["Work on nasal vowels", "Practice the French 'r'"],
            'de': ["Practice umlauts", "Work on consonant clusters"],
            'ru': ["Focus on palatalization", "Practice hard and soft consonants"]
        }
        
        if language in language_tips:
            tips.extend(language_tips[language])
        
        return tips[:4]  # Return top 4 tips

class UniversalTranslatorCore:
    """Core translation engine with universal language support"""
    
    def __init__(self):
        self.translator = Translator()
        self.language_db = UniversalLanguageDatabase()
        self.audio_manager = AdvancedAudioManager()
        self.initialize_enhanced_database()
        
        # Translation confidence thresholds
        self.confidence_thresholds = {
            'high': 0.9,
            'medium': 0.7,
            'low': 0.5
        }
        
        # Context analysis patterns
        self.context_patterns = {
            'formal': ['sir', 'madam', 'please', 'thank you', 'excuse me'],
            'informal': ['hey', 'hi', 'yeah', 'cool', 'awesome'],
            'business': ['meeting', 'presentation', 'proposal', 'contract'],
            'academic': ['research', 'study', 'analysis', 'theory', 'hypothesis'],
            'medical': ['doctor', 'patient', 'symptoms', 'treatment', 'diagnosis'],
            'technical': ['algorithm', 'software', 'hardware', 'system', 'database']
        }
    
    def initialize_enhanced_database(self):
        """Initialize comprehensive database for universal translation"""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Universal vocabulary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS universal_vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                original_language TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                target_language TEXT NOT NULL,
                context_category TEXT,
                confidence_score REAL,
                phonetic_original TEXT,
                phonetic_translation TEXT,
                language_family_original TEXT,
                language_family_target TEXT,
                difficulty_level INTEGER,
                cultural_notes TEXT,
                usage_examples TEXT,
                learned_timestamp TEXT,
                review_count INTEGER DEFAULT 0,
                mastery_score REAL DEFAULT 0.0,
                pronunciation_score REAL DEFAULT 0.0,
                audio_generated BOOLEAN DEFAULT FALSE,
                user_rating INTEGER DEFAULT 0,
                frequency_rank INTEGER,
                semantic_category TEXT
            )
        ''')
        
        # Language pair analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS language_pair_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_language TEXT,
                target_language TEXT,
                translation_count INTEGER DEFAULT 0,
                average_confidence REAL DEFAULT 0.0,
                user_satisfaction REAL DEFAULT 0.0,
                common_errors TEXT,
                improvement_suggestions TEXT,
                last_updated TEXT
            )
        ''')
        
        # Conversation context tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                conversation_turn INTEGER,
                original_message TEXT,
                detected_language TEXT,
                translated_message TEXT,
                target_language TEXT,
                context_type TEXT,
                sentiment_score REAL,
                formality_level TEXT,
                topic_category TEXT,
                timestamp TEXT
            )
        ''')
        
        # Multilingual learning progress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS multilingual_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_session TEXT,
                language_code TEXT,
                words_learned INTEGER DEFAULT 0,
                sentences_translated INTEGER DEFAULT 0,
                audio_exercises_completed INTEGER DEFAULT 0,
                pronunciation_accuracy REAL DEFAULT 0.0,
                comprehension_score REAL DEFAULT 0.0,
                fluency_level TEXT DEFAULT 'beginner',
                total_study_time INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                achievements TEXT,
                last_activity TEXT
            )
        ''')
        
        self.conn.commit()
    
    @lru_cache(maxsize=1000)
    def detect_language_cached(self, text):
        """Cached language detection for performance"""
        return self.audio_manager.detect_language(text)
    
    def universal_translate(self, text, target_language=None, source_language='auto', context='general'):
        """Universal translation with advanced features"""
        try:
            # Auto-detect source language if needed
            if source_language == 'auto' or st.session_state.auto_detect_language:
                detected_lang = self.detect_language_cached(text)
                source_language = detected_lang
                
                # Update detection history
                st.session_state.language_detection_history.append({
                    'text': text[:100],
                    'detected_language': detected_lang,
                    'confidence': self.get_detection_confidence(text, detected_lang),
                    'timestamp': datetime.datetime.now().isoformat()
                })
            
            # Determine target language
            if not target_language:
                target_language = st.session_state.get('primary_language', 'en')
                if source_language == target_language:
                    # Pick a different target from user's target languages
                    target_languages = st.session_state.get('target_languages', ['es', 'fr', 'de'])
                    target_language = target_languages[0] if target_languages else 'es'
            
            # Perform translation
            if source_language == target_language:
                translation_result = text  # No translation needed
                confidence = 1.0
            else:
                translated = self.translator.translate(text, src=source_language, dest=target_language)
                translation_result = translated.text
                confidence = getattr(translated, 'confidence', 0.8)  # Some APIs don't provide confidence
            
            # Analyze context
            detected_context = self.analyze_context(text)
            
            # Generate comprehensive result
            result = {
                'original_text': text,
                'translated_text': translation_result,
                'source_language': source_language,
                'target_language': target_language,
                'confidence': confidence,
                'context': detected_context,
                'source_lang_info': self.language_db.supported_languages.get(source_language, {}),
                'target_lang_info': self.language_db.supported_languages.get(target_language, {}),
                'phonetic_guide': self.generate_phonetic_guide_universal(translation_result, target_language),
                'cultural_insights': self.get_cultural_insights_universal(text, source_language, target_language),
                'example_usage': self.generate_usage_examples(translation_result, target_language, detected_context),
                'difficulty_assessment': self.assess_translation_difficulty(text, translation_result, source_language, target_language),
                'word_breakdown': self.analyze_word_breakdown(text, translation_result, source_language, target_language),
                'grammar_notes': self.get_grammar_notes(source_language, target_language),
                'pronunciation_tips': self.get_pronunciation_tips(target_language),
                'related_phrases': self.get_related_phrases(text, target_language),
                'formality_level': self.assess_formality(text),
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # Store in database
            self.store_translation_result(result)
            
            # Generate audio if enabled
            if st.session_state.audio_enabled:
                result['audio_file'] = self.audio_manager.generate_universal_tts(
                    translation_result, 
                    target_language, 
                    st.session_state.speech_speed
                )
                #result['source']
                result['audio_file_source'] = self.audio_manager.generate_universal_tts(
                    text,
                    source_language,
                    st.session_state.speech_speed
                )
            return result

        except Exception as e:
            st.error(f"Translation error: {e}")
            return {
                'original_text': text,
                'translated_text': '',
                'source_language': source_language,
                'target_language': target_language,
                'confidence': 0.0,
                'context': 'general',
                'error': str(e)
            }

    def analyze_context(self, text):
        """Analyze the context of the given text"""
        context_scores = {
            context_type: sum(1 for pattern in patterns if pattern.lower() in text.lower())
            for context_type, patterns in self.context_patterns.items()
        }
        if any(context_scores.values()):
            primary_context = max(context_scores.items(), key=lambda x: x[1])[0]
        else:
            primary_context = 'general'
        return primary_context

    def generate_phonetic_guide_universal(self, text, language):
        """Generate a simple phonetic guide (placeholder)"""
        # In production, use a real phonetic library or API
        return text  # Placeholder: just returns the text

    def get_cultural_insights_universal(self, text, source_lang, target_lang):
        """Get cultural notes for the target language"""
        notes = []
        cultural_notes = self.language_db.cultural_contexts.get('cultural_notes', {})
        if target_lang in cultural_notes:
            notes.append(cultural_notes[target_lang])
        return notes

    def generate_usage_examples(self, translation_result, target_language, context):
        """Generate example usage (placeholder)"""
        # In production, use a real example sentence generator or corpus
        return [f"Example: {translation_result}"]

    def assess_translation_difficulty(self, source_text, translated_text, source_lang, target_lang):
        """Assess translation difficulty (simple heuristic)"""
        source_info = self.language_db.supported_languages.get(source_lang, {})
        target_info = self.language_db.supported_languages.get(target_lang, {})
        level = 1
        if source_info.get('family') != target_info.get('family'):
            level += 2
        if source_info.get('script') != target_info.get('script'):
            level += 1
        if len(source_text.split()) > 10:
            level += 1
        return {'level': min(level, 5)}

    def analyze_word_breakdown(self, source_text, translated_text, source_lang, target_lang):
        """Break down words for learning (simple split)"""
        return {
            'source_words': source_text.split(),
            'translated_words': translated_text.split()
        }

    def get_grammar_notes(self, source_lang, target_lang):
        """Return grammar notes (placeholder)"""
        return f"Grammar notes for {source_lang} → {target_lang}."

    def get_pronunciation_tips(self, target_lang):
        """Return pronunciation tips (placeholder)"""
        return f"Pronunciation tips for {target_lang}."

    def get_related_phrases(self, text, target_lang):
        """Return related phrases (placeholder)"""
        return []

    def assess_formality(self, text):
        """Assess formality (simple heuristic)"""
        if any(word in text.lower() for word in ['sir', 'madam', 'please', 'thank you']):
            return 'formal'
        elif any(word in text.lower() for word in ['hey', 'hi', 'yeah']):
            return 'informal'
        else:
            return 'neutral'

    def store_translation_result(self, result):
        """Store translation result in the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO universal_vocabulary (
                    original_text,
                    original_language,
                    translated_text,
                    target_language,
                    context_category,
                    confidence_score,
                    phonetic_original,
                    phonetic_translation,
                    language_family_original,
                    language_family_target,
                    difficulty_level,
                    cultural_notes,
                    usage_examples,
                    learned_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.get('original_text', ''),
                result.get('source_language', ''),
                result.get('translated_text', ''),
                result.get('target_language', ''),
                result.get('context', ''),
                result.get('confidence', 0.0),
                '',  # phonetic_original placeholder
                result.get('phonetic_guide', ''),
                result.get('source_lang_info', {}).get('family', ''),
                result.get('target_lang_info', {}).get('family', ''),
                result.get('difficulty_assessment', {}).get('level', 1),
                json.dumps(result.get('cultural_insights', [])),
                json.dumps(result.get('example_usage', [])),
                result.get('timestamp', '')
            ))
            self.conn.commit()
        except Exception as e:
            st.error(f"Database error: {e}")
    def main():
        """Main Streamlit application"""
        st.title("🌐 Universal Language Translator")
    
        # Initialize translator
        translator = UniversalTranslatorCore()

        # Sidebar for language selection
        st.sidebar.header("Settings")
        source_lang = st.sidebar.selectbox(
        "Source Language",
        options=['auto'] + list(translator.language_db.supported_languages.keys()),
        format_func=lambda x: f"{translator.language_db.supported_languages.get(x, {}).get('flag', '')} {translator.language_db.supported_languages.get(x, {}).get('name', x)}" if x != 'auto' else '🔄 Auto Detect'
    )
    
       target_lang = st.sidebar.selectbox(
          "Target Language",
           options=list(translator.language_db.supported_languages.keys()),
          format_func=lambda x: f"{translator.language_db.supported_languages.get(x, {}).get('flag', '')} {translator.language_db.supported_languages.get(x, {}).get('name', x)}"
    )
    
    # Main translation interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Enter Text")
        input_text = st.text_area("", height=150, placeholder="Type or paste text here...")
        
        if st.button("Translate"):
            if input_text:
                with st.spinner("Translating..."):
                    result = translator.universal_translate(
                        text=input_text,
                        source_language=source_lang,
                        target_language=target_lang
                    )
                    
                    if 'error' not in result:
                        st.session_state['last_translation'] = result
    
    with col2:
        st.markdown("### Translation")
        if 'last_translation' in st.session_state:
            result = st.session_state['last_translation']
            
            st.markdown(f"""
            <div class='universal-translation-result'>
                <p>{result['translated_text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show confidence score
            confidence = int(result['confidence'] * 100)
            st.markdown(f"""
            <div class='language-confidence-meter'>
                <div class='confidence-indicator'>{confidence}% Confidence</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Audio controls
            if st.session_state.audio_enabled and 'audio_file' in result:
                st.markdown("### 🔊 Listen")
                translator.audio_manager.play_audio_streamlit(result['audio_file'])
    
    # Additional features section
    if 'last_translation' in st.session_state:
        st.markdown("---")
        result = st.session_state['last_translation']
        
        # Cultural insights
        with st.expander("🎭 Cultural Insights"):
            for insight in result['cultural_insights']:
                st.markdown(f"• {insight}")
        
        # Pronunciation guide
        with st.expander("🗣️ Pronunciation Guide"):
            st.markdown(result['phonetic_guide'])
            st.markdown(result['pronunciation_tips'])
        
        # Usage examples
        with st.expander("📝 Usage Examples"):
            for example in result['example_usage']:
                st.markdown(f"• {example}")

if __name
__ == "__main__":
    main()