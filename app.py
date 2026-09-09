import gradio as gr
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from main import handle_submission, handle_daily_summary

custom_css = """
#step-log textarea { font-family: monospace; font-size: 13px; line-height: 1.4; }
.card-box { background-color: var(--background-fill-secondary); border-radius: 8px; padding: 12px; }
"""

with gr.Blocks(title="Incident & Damage Triage Control Center", css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📦 Shipment Incident & Damage Triage Console")
    gr.Markdown("Submit damage reports to trigger NLP parsing, SLA evaluation, automated decision routing, and daily logs.")

    with gr.Row():
        # Left Column: Input Form
        with gr.Column(scale=1):
            gr.Markdown("### 📥 Submit Damage Report")
            report_input = gr.Textbox(
                label="Incident Report / Claim Text",
                placeholder="e.g., The pallet arrived crushed and 3 boxes of medical monitors are shattered with liquid leakage.",
                lines=4
            )
            name_input = gr.Textbox(
                label="Customer Name",
                placeholder="e.g., John Doe",
                lines=1
            )
            email_input = gr.Textbox(
                label="Customer Email",
                placeholder="e.g., john.doe@example.com",
                lines=1
            )
            tracking_Id_input = gr.Textbox(
                label="Tracking ID",
                placeholder="e.g., TRK123456789",
                lines=1
            )
            val_input = gr.Number(
                label="Shipment Value ($ USD)",
                value=1250.00,
                minimum=0.0
            )
            Shipment_input = gr.DateTime(
                label="Shipment Date",
                value="2024-06-01"
            )
            Delivery_input = gr.DateTime(
                label="Delivery Date",
                value="2024-06-05"
            )
            submit_btn = gr.Button("🚀 Process Incident", variant="primary")

        # Right Column: Outcome & Execution Steps
        with gr.Column(scale=1):
            gr.Markdown("### 🎯 Pipeline Outcome")
            outcome_output = gr.Markdown(value="_Submit a report on the left to view triage results._", elem_classes=["card-box"])
            
            

    gr.Markdown("---")

    # Bottom Area: Daily Log Table & Summary Engine
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 📋 Daily Triage Log")
            triage_table = gr.DataFrame(
                value=pd.DataFrame(columns=["Tracking Id","Category", "Compensation", "Is Escalated"]),
                interactive=False
            )
        with gr.Column(scale=1):
            gr.Markdown("### 📑 Operations Summary")
            summary_btn = gr.Button("🔄 Generate Daily Summary", variant="secondary")
            summary_output = gr.Markdown(value="_Click button above to aggregate today's metrics._")

    # Wire event listeners
    submit_btn.click(
        fn=handle_submission,
        inputs=[report_input, val_input, Shipment_input, Delivery_input, name_input, email_input, tracking_Id_input],
        outputs=[outcome_output, triage_table]
    )

    summary_btn.click(
        fn=handle_daily_summary,
        inputs=[],
        outputs=[summary_output]
    )

# Launch
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=True)