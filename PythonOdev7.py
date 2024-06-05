from flask import Flask, render_template, redirect, url_for, send_from_directory, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import random
import time

matplotlib.use('Agg')

app = Flask(__name__)

def create_plot():
    try:
        print("Plot oluşturma başladı")
        # Rastgele 1000 x ve y koordinatları üretme
        x = np.random.randint(0, 1001, 1000)
        y = np.random.randint(0, 1001, 1000)
        print(f"Yeni noktalar oluşturuldu: x[:5]={x[:5]}, y[:5]={y[:5]}")  # İlk 5 noktayı göster

        # Koordinatları bir DataFrame'e kaydetme
        df = pd.DataFrame({'x': x, 'y': y})

        # Grafik oluşturma
        fig, ax = plt.subplots(figsize=(10, 10))

        # 50*50, 100*100 veya 200*200 şeklinde ızgaralar oluşturma
        grid_size = 50  # Burayı 50, 100 veya 200 olarak değiştirebiliriz

        # Her bir ızgaradaki noktaları farklı renklerde gösterme
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        for i in range(0, 1000, grid_size):
            for j in range(0, 1000, grid_size):
                points_in_grid = df[(df['x'] >= i) & (df['x'] < i + grid_size) & (df['y'] >= j) & (df['y'] < j + grid_size)]
                if not points_in_grid.empty:
                    color = np.random.choice(colors)
                    ax.scatter(points_in_grid['x'], points_in_grid['y'], c=color, alpha=0.5)

        print("Grafik oluşturuldu")

        # Grafik üzerinde ızgaraları gösterme
        plt.xticks(np.arange(0, 1001, grid_size))
        plt.yticks(np.arange(0, 1001, grid_size))
        plt.grid(True)

        plt.title('Rastgele Noktalar ve Izgara')
        plt.xlabel('X Koordinatları')
        plt.ylabel('Y Koordinatları')

        # Dosya adı oluşturma (benzersiz)
        timestamp = int(time.time())
        filename = f'scatter_plot_with_grid_{timestamp}.jpg'
        save_path = os.path.join(app.root_path, filename)

        print(f"Dosya kaydediliyor: {save_path}")

        # Dosyayı kaydetme
        plt.savefig(save_path)
        plt.close()

        # Dosyanın gerçekten oluşturulup oluşturulmadığını kontrol etme
        if os.path.exists(save_path):
            print(f"Görsel başarıyla oluşturuldu: {save_path}")
        else:
            print(f"Dosya oluşturulamadı: {save_path}")

        return filename
    
    except Exception as e:
        print(f"Hata: {e}")
        return None

@app.route('/')
def index():
    plot_filename = request.args.get('plot_filename')
    rand_value = request.args.get('random')
    print(f"index: plot_filename={plot_filename}, random={rand_value}")
    return render_template('index.html', name="Serkan", surname="Yıldırım", student_number="211220028", plot_filename=plot_filename, random=rand_value)

@app.route('/new_plot')
def new_plot():
    plot_filename = create_plot()  # Yeni plot oluştur
    if plot_filename is None:
        return "Görsel oluşturulamadı", 500
    rand_value = random.randint(1, 1000000)
    print(f"Yönlendiriliyor: plot_filename={plot_filename}, random={rand_value}")
    return redirect(url_for('index', plot_filename=plot_filename, random=rand_value))

@app.route('/<filename>')
def serve_file(filename):
    try:
        print(f"Görsel sunuluyor: {filename}")
        file_path = os.path.join(app.root_path, filename)
        if not os.path.exists(file_path):
            print(f"Dosya bulunamadı: {file_path}")
            return "Dosya bulunamadı", 404
        response = send_from_directory(app.root_path, filename)
        print(f"Görsel sunuldu: {filename}")
        return response
    except Exception as e:
        print(f"Görsel sunulamadı: {filename}, Hata: {e}")
        return "Görsel sunulamadı", 404

if __name__ == '__main__':
    app.run(debug=True)
