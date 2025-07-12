import gradio as gr
import pandas as pd
import requests
import json

from dotenv import load_dotenv
load_dotenv()
import os
CHARTS_DATA_API = os.getenv('CHARTS_DATA_API')
CHART_DATA_SERIES_API = os.getenv('CHART_DATA_SERIES_API')

def get_all_charts():
    """Retrieve all MM Charts data to search a most relevant one
    """
    df = pd.read_csv('chart.csv')
    return df.iloc[:,:2].to_json(orient='records', force_ascii=False)

def get_one_chart(chart_id):
    """Retrieve one MM Chart data: chart_info, series_sample, and series API to call from the frontend.
    Args:
        chart_id: The id of the MM Chart data to retrieve
    Returns:
        a MM Chart chart_info and series_sample for coding the highchart,
        and the series API to call to get the complete series from the frontend.
    """
    r = requests.get(f'{CHARTS_DATA_API}/{chart_id}')
    data = r.json()
    chart_info = data['data'][f'c:{chart_id}']['info']
    series_sample = data['data'][f'c:{chart_id}']['series']
    for i in range(len(series_sample)):
        series_sample[i] = series_sample[i][:10]
    # return json.dumps(data, ensure_ascii=False)
    return (
        json.dumps(chart_info, ensure_ascii=False),
        json.dumps(series_sample),
        f'{CHART_DATA_SERIES_API}/series?chart_id={chart_id}')

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            get_charts_data_btn = gr.Button("GET", interactive=False)
            charts_data_output = gr.Textbox(label="MM Charts data", lines=10)
            
            get_charts_data_btn.click(
                fn=get_all_charts,
                outputs=charts_data_output
            )
        with gr.Column():
            chart_id_input = gr.Textbox(label="chart_id", interactive=False)
            chart_info_output = gr.Textbox(label="MM Chart info")
            series_sample_output = gr.Textbox(label="MM Chart series sample")
            series_api_output = gr.Textbox(label="MM Chart series API")
            
            chart_id_input.change(
                fn=get_one_chart,
                inputs=chart_id_input,
                outputs=[chart_info_output, series_sample_output, series_api_output]
            )

if __name__ == "__main__":
    demo.launch()