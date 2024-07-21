"""
Streamlit application for processing images with custom configurations.

This module provides a Streamlit-based web interface for uploading images and configuration files,
processing the images using specified pipelines, and displaying the results. Users can either
upload their own configuration files or use a default configuration.
"""

import argparse

import streamlit as st
from main import load_prompts_config, create_valid_json
from config import AppConfig
from analysis import processA, processB, processC

# Path to the default configuration file.
DEFAULT_CONFIG_PATH = 'analysis/prompts/data.yaml'


def run_streamlit(image_file: str, heatmap_image_file: str, prompts_config: dict) -> str:
    """
    Run the Streamlit application to process images and display results.

    Args:
        image_file (str): Path to the uploaded image file.
        heatmap_image_file (str): Path to the uploaded heatmap image file.
        prompts_config (dict): Configuration dictionary for the processing pipelines.

    Returns:
        str: The JSON-formatted result of the final processing stage.
    """
    st.subheader("Image Preview")
    st.image(image_file, use_column_width=True)
    image_path = image_file.name
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())

    heatmap_image_path = heatmap_image_file.name
    st.subheader("Heatmap Image Preview")
    st.image(heatmap_image_file, use_column_width=True)
    with open(heatmap_image_path, "wb") as f:
        f.write(heatmap_image_file.getbuffer())

    # Process A
    st.write("Running Process A...")
    a_output = processA.pipeline(prompts_config["a_process"], image_path, heatmap_image_path)
    st.write("Process A Results:")
    st.write(a_output)

    # Process B
    st.write("Running Process B...")
    b_output = processB.pipeline(prompts_config["b_process"], image_path)
    st.write("Process B Results:")
    st.write(b_output)

    # Process C
    st.write("Running Process C...")
    c_output = processC.pipeline(prompts_config["c_process"], a_output, b_output)
    st.write("Process C Results:")
    st.write(c_output)

    result_json = create_valid_json(c_output)

    st.write("Final Result:")
    st.json(result_json)
    return result_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Main')
    parser.add_argument('--env_path', type=str, default="./envs/.env")
    parser.add_argument('--logger_save_path', type=str, default=".")
    args = parser.parse_args()
    app_config = AppConfig(args.env_path, args.logger_save_path)

    st.title('Processing Application')

    config_file = st.file_uploader("Upload configuration file", type=["yaml", "yml"])
    use_default_config = st.checkbox('Use default configuration if no file is uploaded', value=True)

    image_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    heatmap_image_file = st.file_uploader("Upload heatmap image", type=["jpg", "jpeg", "png"])

    if config_file:
        st.subheader("Configuration File Preview")
        config_text = config_file.read().decode("utf-8")
        st.text_area("Configuration File Content", config_text, height=200)
        config_file.seek(0)  # Reset file pointer to the beginning
        prompts_config = load_prompts_config(config_file)
    elif use_default_config:
        prompts_config = load_prompts_config(DEFAULT_CONFIG_PATH)
        st.write("Using default configuration")

    if st.button('Run Processing'):
        result_json = run_streamlit(image_file, heatmap_image_file, prompts_config)
