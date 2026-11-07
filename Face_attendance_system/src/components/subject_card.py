import streamlit as st
import html

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Escape values received from the database for safety
    name = html.escape(str(name))
    code = html.escape(str(code))
    section = html.escape(str(section))

    # Build the HTML card layout as a single-line or cleanly concatenated string
    card_html = f"""
    <div style="
        background: #ffffff;
        border: 1px solid #dbe0f0;
        border-left: 8px solid #5865F2;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    ">
        <h3 style="
            margin: 0 0 12px 0;
            color: #1e293b;
            font-size: 1.6rem;
            font-weight: 700;
        ">{name}</h3>

        <p style="
            color: #64748b;
            margin: 10px 0 18px 0;
            font-size: 1rem;
        ">
            Subject Code:
            <span style="
                background: #E0E3FF;
                color: #5865F2;
                padding: 5px 10px;
                border-radius: 6px;
                font-weight: 600;
            ">{code}</span>
            &nbsp; | &nbsp;
            Section: <b>{section}</b>
        </p>
    """

    # Add student and class statistics if available
    if stats:
        card_html += """
        <div style="
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 12px;
        ">
        """

        for icon, label, value in stats:
            card_html += f"""
            <div style="
                background: #fce7f3;
                color: #1e293b;
                padding: 10px 14px;
                border-radius: 10px;
                font-size: 0.95rem;
            ">
                {html.escape(str(icon))}
                <b>{html.escape(str(value))}</b>
                {html.escape(str(label))}
            </div>
            """

        card_html += "</div>"

    # Close the wrapper div
    card_html += "</div>"

    # Render using st.html() instead of st.markdown() to avoid code-block interpretation
    st.html(card_html)

    # Display the optional button below the card
    if footer_callback:
        footer_callback()