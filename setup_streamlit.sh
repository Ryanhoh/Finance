mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"ouanane.rn@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "STREAMLIT_CONFIG_LOCATION=$PWD" >> ~/.streamlit/config.toml