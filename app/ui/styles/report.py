from textwrap import dedent


def build_report_css() -> str:
    return dedent(
        f"""
        .report-html-shell,
        .report-html-shell > .gr-block,
        .report-html-shell .gr-group,
        .report-html-shell .gr-box,
        .report-html-shell .gr-panel,
        .report-html-shell .block {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }}

        .report-shell {{
            background: var(--bg-panel-soft);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow-lg);
            padding: 22px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .report-shell-realtime {{
            gap: 20px;
        }}

        .report-view-shell {{
            background: transparent;
        }}

        .report-topbar {{
            position: sticky;
            top: 16px;
            z-index: 4;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            padding: 14px 18px;
            border: 1px solid rgba(30, 41, 59, 0.8);
            border-radius: 18px;
            background: rgba(21, 27, 46, 0.86);
            backdrop-filter: blur(12px);
        }}

        .report-topbar-main {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .report-topbar-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .report-topbar-back,
        .report-download-btn {{
            border: 1px solid rgba(71, 85, 105, 0.85);
            background: rgba(15, 23, 42, 0.84);
            color: #cbd5e1;
            cursor: pointer;
            transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
        }}

        .report-topbar-back:hover,
        .report-download-btn:hover {{
            background: rgba(30, 41, 59, 0.96);
            color: #f8fafc;
            transform: translateY(-1px);
        }}

        .report-topbar-back {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            font-size: 18px;
            line-height: 1;
        }}

        .report-download-btn {{
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
        }}

        .report-topbar h2 {{
            margin: 0;
            font-size: 20px;
            color: #f8fafc;
            letter-spacing: -0.02em;
        }}

        .report-topbar p {{
            margin: 4px 0 0;
            color: #64748b;
            font-size: 12px;
        }}

        .report-summary-grid,
        .report-grid,
        .participant-grid {{
            display: grid;
            gap: 14px;
        }}

        .report-summary-grid {{
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }}

        .report-summary-card,
        .report-card,
        .participant-card {{
            border-radius: 16px;
            border: 1px solid rgba(30, 41, 59, 0.8);
            background: rgba(21, 27, 46, 0.98);
        }}

        .figma-card {{
            box-shadow: none;
        }}

        .report-summary-card {{
            padding: 18px 18px 16px;
            backdrop-filter: blur(12px);
        }}

        .report-summary-label,
        .report-card-head span,
        .participant-head span,
        .report-event-head span {{
            color: var(--text-muted);
            font-size: 11px;
        }}

        .report-summary-value {{
            margin-top: 6px;
            color: var(--text);
            font-size: 30px;
            font-weight: 700;
            letter-spacing: -0.03em;
        }}

        .report-summary-meta {{
            margin-top: 8px;
            color: var(--text-muted);
            font-size: 12px;
            line-height: 1.5;
        }}

        .tone-positive .report-summary-value,
        .tone-positive {{
            color: #34d399;
        }}

        .tone-warning .report-summary-value,
        .tone-warning {{
            color: #fbbf24;
        }}

        .tone-danger .report-summary-value,
        .tone-danger {{
            color: #f87171;
        }}

        .report-grid {{
            grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
        }}

        .report-card {{
            padding: 18px;
            backdrop-filter: blur(12px);
        }}

        .report-chart-card {{
            overflow: hidden;
        }}

        .report-chart-legend {{
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
            color: var(--text-muted);
            font-size: 12px;
        }}

        .report-chart-legend span {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .chart-dot {{
            width: 10px;
            height: 10px;
            border-radius: 999px;
            display: inline-flex;
        }}

        .chart-normal {{
            background: #10b981;
        }}

        .chart-drowsy {{
            background: #f59e0b;
        }}

        .chart-absence {{
            background: #ef4444;
        }}

        .report-chart-wrap {{
            margin-top: 14px;
            min-height: 320px;
            padding: 12px 8px 4px;
            border-radius: 14px;
            border: 1px solid rgba(30, 41, 59, 0.8);
            background: rgba(15, 23, 42, 0.54);
        }}

        .report-area-chart {{
            position: relative;
            width: 100%;
            height: 268px;
        }}

        .report-area-chart::after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(59, 130, 246, 0.04), transparent 40%);
            pointer-events: none;
        }}

        .report-area-svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        .chart-grid-line {{
            stroke: rgba(148, 163, 184, 0.14);
            stroke-width: 1;
        }}

        .chart-axis-label {{
            fill: #64748b;
            font-size: 11px;
        }}

        .area-normal-fill {{
            fill: rgba(16, 185, 129, 0.20);
            animation: areaReveal 0.85s ease-out both;
            transform-origin: bottom;
        }}

        .area-drowsy-fill {{
            fill: rgba(245, 158, 11, 0.22);
            animation: areaReveal 0.95s ease-out both;
            transform-origin: bottom;
        }}

        .area-absence-fill {{
            fill: rgba(239, 68, 68, 0.20);
            animation: areaReveal 1.05s ease-out both;
            transform-origin: bottom;
        }}

        .area-normal-line,
        .area-drowsy-line,
        .area-absence-line {{
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-width: 2.5;
            stroke-dasharray: 1200;
            stroke-dashoffset: 1200;
            animation: chartLineDraw 1.1s ease-out forwards;
        }}

        .area-normal-line {{
            stroke: #10b981;
        }}

        .area-drowsy-line {{
            stroke: #f59e0b;
        }}

        .area-absence-line {{
            stroke: #ef4444;
        }}

        .report-chart-label {{
            color: var(--text-muted);
            font-size: 11px;
            text-align: center;
            white-space: nowrap;
        }}

        .report-card-head,
        .participant-head,
        .report-event-head {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
        }}

        .report-event-list,
        .participant-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 12px;
        }}

        .report-event {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid rgba(30, 41, 59, 0.75);
            background: rgba(8, 13, 24, 0.28);
        }}

        .report-event-icon {{
            width: 34px;
            height: 34px;
            flex: 0 0 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: rgba(15, 23, 42, 0.72);
            font-size: 13px;
        }}

        .report-event-label {{
            font-size: 12px;
            font-weight: 600;
        }}

        .report-event-time {{
            color: #94a3b8;
            font-size: 10px;
        }}

        .report-event-copy {{
            flex: 1;
            min-width: 0;
        }}

        .participant-head strong,
        .report-event-head strong {{
            color: var(--text);
            font-size: 14px;
        }}

        .participant-meta span,
        .report-event p,
        .report-highlight-list li {{
            color: var(--text-muted);
            font-size: 13px;
            line-height: 1.6;
        }}

        .report-highlight-list {{
            margin: 0;
            padding-left: 0;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .report-event p {{
            margin: 5px 0 0;
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.45;
        }}

        .report-event-participant {{
            margin-top: 5px;
            color: #475569;
            font-size: 11px;
        }}

        .report-event.tone-positive {{
            background: var(--green-soft);
            border-color: rgba(16, 185, 129, 0.24);
        }}

        .report-event.tone-warning {{
            background: var(--amber-soft);
            border-color: rgba(245, 158, 11, 0.24);
        }}

        .report-event.tone-danger {{
            background: var(--red-soft);
            border-color: rgba(239, 68, 68, 0.24);
        }}

        .report-animate {{
            opacity: 0;
            transform: translateY(18px);
            animation: reportCardIn 0.55s ease-out forwards;
        }}

        .report-summary-grid .report-animate:nth-child(1) {{ animation-delay: 0.04s; }}
        .report-summary-grid .report-animate:nth-child(2) {{ animation-delay: 0.09s; }}
        .report-summary-grid .report-animate:nth-child(3) {{ animation-delay: 0.14s; }}
        .report-summary-grid .report-animate:nth-child(4) {{ animation-delay: 0.19s; }}
        .report-grid .report-animate:nth-child(1) {{ animation-delay: 0.22s; }}
        .report-grid .report-animate:nth-child(2) {{ animation-delay: 0.28s; }}
        .participant-grid .report-animate:nth-child(1) {{ animation-delay: 0.30s; }}
        .participant-grid .report-animate:nth-child(2) {{ animation-delay: 0.34s; }}
        .participant-grid .report-animate:nth-child(3) {{ animation-delay: 0.38s; }}

        .report-insight-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }}

        .report-insight {{
            padding: 16px;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(8, 13, 24, 0.38);
        }}

        .report-insight strong {{
            color: var(--text);
            font-size: 14px;
        }}

        .report-insight p {{
            margin: 8px 0 0;
            color: var(--text-soft);
            font-size: 13px;
            line-height: 1.6;
        }}

        .report-insight.tone-info {{
            background: rgba(37, 99, 235, 0.08);
            border-color: rgba(96, 165, 250, 0.22);
        }}

        .report-insight.tone-warning {{
            background: rgba(245, 158, 11, 0.08);
            border-color: rgba(245, 158, 11, 0.22);
        }}

        @keyframes chartLineDraw {{
            to {{
                stroke-dashoffset: 0;
            }}
        }}

        @keyframes areaReveal {{
            from {{
                opacity: 0;
                transform: translateY(18px) scaleY(0.92);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scaleY(1);
            }}
        }}

        @keyframes reportCardIn {{
            from {{
                opacity: 0;
                transform: translateY(18px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .report-placeholder,
        .report-empty {{
            padding: 22px;
            border-radius: 16px;
            text-align: center;
            background: rgba(21, 27, 46, 0.96);
            border: 1px solid rgba(30, 41, 59, 0.8);
            color: var(--text-muted);
        }}

        .report-empty h2 {{
            margin: 0 0 8px;
            color: var(--text);
        }}

        .participant-card {{
            padding: 14px;
        }}

        .participant-bar {{
            margin-top: 10px;
            display: flex;
            height: 7px;
            border-radius: 999px;
            overflow: hidden;
            background: rgba(51, 65, 85, 0.8);
        }}

        .participant-bar .tone-positive {{
            background: var(--green);
        }}

        .participant-bar .tone-warning {{
            background: var(--amber);
        }}

        .participant-bar .tone-danger {{
            background: var(--red);
        }}

        .participant-meta {{
            margin-top: 8px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            color: var(--text-muted);
            font-size: 11px;
        }}

        .report-card-head h3 {{
            margin: 0;
            color: var(--text);
            font-size: 18px;
            font-weight: 700;
        }}

        .report-card-head h3 {{
            margin: 0;
            font-size: 17px;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }}

        .report-chart-card .report-card-head h3 {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .report-insight-grid {{
            gap: 12px;
        }}

        .report-insight {{
            padding: 14px;
            border-radius: 14px;
        }}

        .report-insight strong {{
            font-size: 13px;
        }}

        .report-insight p {{
            margin-top: 6px;
            font-size: 12px;
            line-height: 1.5;
        }}

        @media (max-width: 1024px) {{
            .report-summary-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .report-grid,
            .report-insight-grid,
            .live-layout,
            .upload-layout {{
                grid-template-columns: 1fr !important;
            }}
        }}

        @media (max-width: 768px) {{
            #app-root {{
                padding: 10px 14px 20px !important;
            }}

            .shell-header,
            .home-hero,
            .live-layout,
            .upload-layout,
            .report-actions {{
                padding-left: 16px !important;
                padding-right: 16px !important;
            }}

            #home-card-grid,
            .home-card-grid {{
                padding-left: 16px !important;
                padding-right: 16px !important;
            }}

            .shell-header,
            .shell-header-main,
            .report-topbar,
            .report-topbar-main {{
                flex-direction: column;
            }}

            .shell-copy h1,
            .home-hero h1,
            .report-topbar h2 {{
                font-size: 36px;
            }}

            .hero-note {{
                font-size: 18px;
            }}

            .mode-card {{
                height: auto;
                min-height: 560px;
                max-height: none;
                padding: 28px;
            }}

            #home-hero-section,
            .home-hero {{
                padding-top: 0;
            }}

            #home-card-grid,
            .home-card-grid {{
                grid-template-columns: 1fr !important;
                padding-top: 20px !important;
            }}

            #home-footer-section,
            .home-footer {{
                padding-top: 20px;
                padding-bottom: 0;
            }}

            .report-summary-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        """
    )
