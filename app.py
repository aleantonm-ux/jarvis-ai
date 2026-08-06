import os
from flask import Flask, render_template_string, request, jsonify
from groq import Groq

app = Flask(__name__)

# Template HTML con interfaccia HUD / FUI in stile Stark Tech / Spider-Man
HUD_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E.V. // HUD Interface</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

        :root {
            --primary-color: #00ffff;
            --alert-color: #ff3333;
            --bg-transparent: rgba(2, 6, 23, 0.6);
            --border-glow: 0 0 10px rgba(0, 255, 255, 0.4);
        }

        body {
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            background-color: #010409;
            color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace;
            overflow: hidden;
            box-sizing: border-box;
        }

        /* Maschera HUD con effetto vignettatura e linee di scansione */
        .hud-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: radial-gradient(circle, transparent 60%, rgba(0, 0, 0, 0.8) 100%),
                        linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
            background-size: 100% 4px;
            z-index: 100;
        }

        /* CENTRO LIBERO E PULITO */
        .center-viewport {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 400px;
            pointer-events: none;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Mirino Centrale Dinamico */
        .targeting-reticle {
            width: 120px;
            height: 120px;
            border: 1px dashed rgba(0, 255, 255, 0.3);
            border-radius: 50%;
            position: relative;
            animation: rotate-reticle 20s linear infinite;
        }
        .targeting-reticle::before {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 6px; height: 6px;
            background-color: var(--primary-color);
            box-shadow: var(--border-glow);
        }
        @keyframes rotate-reticle {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* POSIZIONAMENTO PERIFERICO (ANGOLI E LATI) */
        .hud-panel {
            position: absolute;
            background: var(--bg-transparent);
            border: 1px solid rgba(0, 255, 255, 0.3);
            padding: 12px 16px;
            backdrop-filter: blur(2px);
            box-shadow: var(--border-glow);
            font-size: 0.85rem;
            letter-spacing: 1px;
            z-index: 10;
        }

        /* Angolo in alto a sinistra: Stato del sistema e API Key */
        .top-left {
            top: 20px;
            left: 20px;
            width: 280px;
        }

        /* Angolo in alto a destra: Telemetria / CPU */
        .top-right {
            top: 20px;
            right: 20px;
            width: 220px;
        }

        /* Angolo in basso a sinistra: Mini Radar Circolare */
        .bottom-left {
            bottom: 20px;
            left: 20px;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle, rgba(0,255,255,0.05) 0%, rgba(2,6,23,0.8) 80%);
        }
        .radar-sweep {
            width: 100px; height: 100px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            border-radius: 50%;
            position: relative;
            overflow: hidden;
        }
        .radar-sweep::after {
            content: '';
            position: absolute;
            top: 0; left: 50%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3));
            transform-origin: left center;
            animation: radar-spin 4s linear infinite;
        }
        @keyframes radar-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Angolo in basso a destra: Storico Chat / Risposte IA */
        .bottom-right {
            bottom: 20px;
            right: 20px;
            width: 380px;
            max-height: 250px;
            display: flex;
            flex-direction: column;
        }
        .chat-log {
            flex: 1;
            overflow-y: auto;
            max-height: 160px;
            margin-bottom: 10px;
            font-size: 0.8rem;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .chat-msg.user { color: #a5f3fc; }
        .chat-msg.ai { color: var(--primary-color); }

        /* Barra di input inferiore centrata ma ancorata in basso */
        .bottom-input-bar {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 450px;
            background: var(--bg-transparent);
            border: 1px solid rgba(0, 255, 255, 0.4);
            padding: 8px 12px;
            display: flex;
            gap: 8px;
            z-index: 20;
            box-shadow: var(--border-glow);
        }
        .bottom-input-bar input {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--primary-color);
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9rem;
            outline: none;
        }
        .bottom-input-bar button {
            background: rgba(0, 255, 255, 0.2);
            border: 1px solid var(--primary-color);
            color: var(--primary-color);
            padding: 4px 12px;
            cursor: pointer;
            font-family: 'Share Tech Mono', monospace;
        }
        .bottom-input-bar button:hover {
            background: var(--primary-color);
            color: #010409;
        }

        /* Barre di stato verticali */
        .stat-bar-container {
            width: 100%;
            background: rgba(255,255,255,0.1);
            height: 6px;
            margin-top: 4px;
        }
        .stat-bar-fill {
            height: 100%;
            background: var(--primary-color);
            width: 75%;
            box-shadow: var(--border-glow);
        }

        input[type="password"] {
            background: rgba(0,0,0,0.5);
            border: 1px solid var(--primary-color);
            color: var(--primary-color);
            padding: 4px;
            width: 95%;
            font-family: 'Share Tech Mono', monospace;
        }
    </style>
</head>
<body>

    <div class="hud-overlay"></div>

    <div class="center-viewport">
        <div class="targeting-reticle"></div>
    </div>

    <div class="hud-panel top-left">
        <div style="margin-bottom: 6px; color: #fff; font-weight: bold;">[CONFIGURAZIONE SISTEMA]</div>
        <label>GROQ API KEY:</label><br>
        <input type="password" id="apiKeyInput" placeholder="Inserisci chiave..." value="{{ api_key }}">
    </div>

    <div class="hud-panel top-right">
        <div style="color: #fff; font-weight: bold; margin-bottom: 4px;">[TELEMETRIA]</div>
        <div>CPU LOAD: <span id="cpuLoad">42</span>%</div>
        <div class="stat-bar-container"><div class="stat-bar-fill" style="width: 42%;"></div></div>
        <div style="margin-top: 6px;">CORE TEMP: 36.4°C</div>
        <div>MODEL: LLAMA-3.3</div>
    </div>

    <div class="hud-panel bottom-left">
        <div style="font-size: 0.75rem; margin-bottom: 6px; color:#fff;">[RADAR TATTICO]</div>
        <div class="radar-sweep"></div>
    </div>

    <div class="hud-panel bottom-right">
        <div style="color: #fff; font-weight: bold; margin-bottom: 6px;">[E.V. // CANALE AUDIO]</div>
        <div class="chat-log" id="chatLog">
            <div class="chat-msg ai">> E.V. online. Inserisci chiave API e invia un comando.</div>
        </div>
    </div>

    <div class="bottom-input-bar">
        <input type="text" id="userInput" placeholder="Inserisci
