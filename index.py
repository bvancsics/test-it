from app import app
from layout import get_layout
import callbacks


app.layout = get_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
