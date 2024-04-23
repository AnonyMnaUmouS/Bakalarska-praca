import argparse
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import combinations
from tkinter import messagebox, PhotoImage, Label, filedialog


class App:
    def __init__(self, root):
        self.edges = None
        self.nodes = None
        self.enter_number_of_tokens = None
        self.number_of_tokens = None
        self.button_save_graph_id = None
        self.button_back_id = None
        self.button_save_id = None
        self.enter_edges = None
        self.edges_label = None
        self.enter_nodes = None
        self.nodes_label = None
        self.root = root
        self.root.title("Graph Application")

        self.graphs = Graph()

        # self.canvas = tk.Canvas(self.root, width=400, height=400)

        self.width = self.root.winfo_screenwidth()-50
        self.height = self.root.winfo_screenheight()-100

        self.root.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        img1 = PhotoImage(file='new_graph.png')
        self.canvas.create_image(self.width / 2, self.height / 2 - img1.height() / 2, image=img1, tags="new_graph")
        self.canvas.tag_bind("new_graph", "<Button-1>", self.new_graph)

        img2 = PhotoImage(file='load_graph.png')
        self.canvas.create_image(self.width / 2, self.height / 2 + img2.height() / 2, image=img2, tags="load_graph")
        self.canvas.tag_bind("load_graph", "<Button-1>", self.load_graph)

        self.canvas.bind('<B1-Motion>', self.move)
        self.canvas.bind('<ButtonPress>', self.klik)

        self.root.mainloop()

    def klik(self, event):
        ...

    def move(self, event):
        index = -1
        for i in range(len(self.graphs.positions)):
            if abs(self.graphs.positions[i][0] - event.x) < 15 and abs(self.graphs.positions[i][1] - event.y) < 15:
                index = i
                break
        if index != -1:
            self.graphs.positions[index] = (event.x, event.y)
            self.draw()

    def button_click(self, a):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        elif self.enter_edges.get("1.0", 'end-1c') == "":
            messagebox.showinfo("Error", "Please enter edges")
        else:
            self.graphs.parse(False, self.enter_nodes.get(), self.enter_edges.get("1.0", 'end-1c'))
            self.prepare_to_draw(False)

    def button_click_token(self, a):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        elif self.enter_edges.get("1.0", 'end-1c') == "":
            messagebox.showinfo("Error", "Please enter edges")
        else:
            def button_click_token(a):
                k = self.enter_number_of_tokens.get()

                self.graphs.parse(True, self.nodes, self.edges, int(k))
                self.prepare_to_draw(True)
            
            self.nodes = self.enter_nodes.get()
            self.edges = self.enter_edges.get("1.0", 'end-1c')
            self.canvas.delete('all')
            self.nodes_label.destroy()
            self.edges_label.destroy()
            self.enter_nodes.destroy()
            self.enter_edges.destroy()

            custom_font = ('Arial', 12)
            self.number_of_tokens = tk.Label(font=custom_font, text='Enter number of tokens:')
            self.number_of_tokens.place(x=20, y=20)
            self.enter_number_of_tokens = tk.Entry(width=60)
            # self.enter_number_of_tokens.insert(tk.END, nodes)
            self.enter_number_of_tokens.place(x=20, y=50)

            img = PhotoImage(file='create_token_graph.png')
            self.canvas.create_image(20 + img.width() / 2, 130, image=img, tags="button")
            self.canvas.tag_bind("button", "<Button-1>", button_click_token)

            self.root.mainloop()


    def prepare_to_draw(self, token):
        self.canvas.delete('all')
        self.nodes_label.destroy()
        self.edges_label.destroy()
        self.enter_nodes.destroy()
        self.enter_edges.destroy()
        if self.number_of_tokens is not None:
            self.number_of_tokens.destroy()
        if self.enter_number_of_tokens is not None:
            self.enter_number_of_tokens.destroy()

        if token:
            graph = self.graphs.token
            layout = nx.spring_layout(self.graphs.token, seed=42)
        else:
            graph = self.graphs.g
            layout = nx.spring_layout(self.graphs.g, seed=42)

        self.graphs.nodes, self.graphs.edges, self.graphs.positions = [], [], []

        for node in graph.nodes():
            x, y = layout[node]
            self.graphs.positions.append((x * 150 + 300, y * 150 + 300))
            self.graphs.nodes.append(node)

        self.graphs.edges = list(graph.edges)

        self.draw()

        img1 = PhotoImage(file='back.png')
        self.button_back_id = self.canvas.create_image(self.width - img1.width() / 2, self.height - img1.height() / 2,
                                                       image=img1, tags="button_back")
        self.canvas.tag_bind(self.button_back_id, "<Button-1>", self.button_back)

        img2 = PhotoImage(file='save.png')
        self.button_save_id = self.canvas.create_image(self.width - img1.width() - img2.width() / 2,
                                                       self.height - img2.height() / 2, image=img2, tags="button_save")
        self.canvas.tag_bind(self.button_save_id, "<Button-1>", self.button_save)

        img3 = PhotoImage(file='save_graph.png')
        self.button_save_graph_id = self.canvas.create_image(self.width - img1.width() - img2.width() - img3.width() / 2,
                                                             self.height - img3.height() / 2, image=img3,
                                                             tags="button_save_graph")
        self.canvas.tag_bind(self.button_save_graph_id, "<Button-1>", self.button_save_graph)

        self.root.mainloop()

    def draw(self):

        for item in self.canvas.find_all():
            if item != self.button_back_id and item != self.button_save_id and item != self.button_save_graph_id:
                self.canvas.delete(item)

        for x, y in self.graphs.edges:
            x = self.graphs.positions[self.graphs.nodes.index(x)]
            y = self.graphs.positions[self.graphs.nodes.index(y)]
            self.canvas.create_line(x[0], x[1], y[0], y[1])

        for i in range(len(self.graphs.nodes)):
            pos = self.graphs.positions[i]
            self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill="#50a5fa", outline="")
            self.canvas.create_text(pos[0], pos[1], text=str(self.graphs.nodes[i]), font=("Arial", 12), fill="black")

    def button_save(self, event):

        filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                title="Save the image as...")

        if filename:
            # Create a blank PIL Image with the same dimensions as the canvas
            img = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), "white")
            draw = ImageDraw.Draw(img)

            # Define font properties
            font = ImageFont.truetype("arial.ttf", 12)  # Change "arial.ttf" to your desired font file

            # Iterate through all canvas items and draw them onto the image
            for item in self.canvas.find_all():
                item_type = self.canvas.type(item)

                print(item, item_type)

                if item_type == "line":
                    x1, y1, x2, y2 = self.canvas.coords(item)
                    draw.line([(x1, y1), (x2, y2)], fill="black")
                elif item_type == "oval":
                    x1, y1, x2, y2 = self.canvas.coords(item)
                    draw.ellipse([(x1, y1), (x2, y2)], fill="#50a5fa")
                elif item_type == "text":
                    x, y = self.canvas.coords(item)
                    text = self.canvas.itemcget(item, "text")
                    text_color = self.canvas.itemcget(item, "fill")
                    draw.text((x, y), text, fill=text_color, font=font)

            # Save the PIL Image as a PNG file
            img.save(filename, "PNG")
            messagebox.showinfo("Success", "Image saved successfully!")

    def button_save_graph(self, event):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("TXT files", "*.txt"), ("All files", "*.*")],
                                                title="Save the graph as...")

        if filename:
            with open(filename, 'w') as file:
                file.write(', '.join(map(str, self.graphs.g.nodes)) + '\n')
                file.write(', '.join(f"({a}, {b})" for a, b in self.graphs.g.edges) + '\n')

                messagebox.showinfo("Success", "Graph saved successfully!")

    def button_back(self, event):
        self.new_graph(event, ', '.join(map(str, self.graphs.g.nodes))
                       , ', '.join(f"({a}, {b})" for a, b in self.graphs.g.edges))

    def new_graph(self, a, nodes="", edges=""):
        self.graphs.nodes = []
        self.graphs.edges = []
        self.graphs.positions = []

        self.canvas.delete('all')
        custom_font = ('Arial', 12)
        self.nodes_label = tk.Label(font=custom_font, text='Enter nodes:')
        self.nodes_label.place(x=20, y=20)

        canvas_width = int(self.width * 0.8)
        entry_width = canvas_width - 20  # Adjust for padding and border
        self.enter_nodes = tk.Entry(width=int(entry_width / 4.9))

        # self.enter_nodes = tk.Entry(width=60)

        self.enter_nodes.insert(tk.END, nodes)
        self.enter_nodes.place(x=20, y=50)

        self.edges_label = tk.Label(font=custom_font, text='Enter edges:')
        self.edges_label.place(x=20, y=100)
        self.enter_edges = tk.Text(self.root, width=int(entry_width / 6.5), height=5)
        self.enter_edges.insert(tk.END, edges)
        self.enter_edges.place(x=20, y=130)

        img1 = PhotoImage(file='create_graph.png')
        self.canvas.create_image(20 + img1.width() / 2, 230 + img1.height() / 2, image=img1, tags="button1")
        self.canvas.tag_bind("button1", "<Button-1>", self.button_click)

        img2 = PhotoImage(file='create_token_graph.png')
        self.canvas.create_image(20 + img1.width() + img2.width() / 2, 230 + img2.height() / 2, image=img2,
                                 tags="button2")
        self.canvas.tag_bind("button2", "<Button-1>", self.button_click_token)

        self.root.mainloop()

    def load_graph(self, a, nodes="", edges=""):
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, 'r') as file:
                nodes = file.readline().strip('\n')
                edges = file.readline().strip('\n')

                print(nodes.split(','))
                print(edges.split(' '))

                self.graphs.parse(False, nodes, edges)
                self.button_back(a)

        else:
            print("No file selected.")
        # self.new_graph(a, nodes, edges)

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


class Graph:
    def __init__(self):
        self.positions = []
        self.nodes = []
        self.edges = []

        self.g = nx.Graph()
        self.token = nx.Graph()

    def parse(self, token, nodes, edges, k=2):

        self.g = nx.Graph()
        self.token = nx.Graph()

        nodes = nodes.replace(' ', '').split(',')

        if "(" in edges:
            edges = edges[1:-1].replace('), ', '),').split('),(')
            edges = [tuple(map(str, t.replace(' ', '').split(','))) for t in edges]
        else:
            edges = edges.split()
            for i in range(len(edges)):
                edges[i] = edges[i].split(",")
                edges[i] = tuple(edges[i])

        self.g.add_nodes_from(nodes)
        self.g.add_edges_from(edges)

        if token:
            self.to_token(k)

    def to_token(self, k):
        node_combinations = list(combinations(self.g.nodes, k))
        self.token.add_nodes_from(node_combinations)

        for nodes1 in self.token.nodes:
            for nodes2 in self.token.nodes:
                if nodes1 != nodes2 and len(set(nodes1).intersection(nodes2)) == k - 1:
                    diff = set(nodes1) ^ set(nodes2)
                    if self.g.has_edge(diff.pop(), diff.pop()):
                        self.token.add_edge(nodes1, nodes2)

    def is_eulerian(self, g):
        return nx.is_eulerian(g)

    def is_tree(self, g):
        return nx.is_tree(g)

    def is_regular(self, g):
        return nx.is_regular(g)

    def is_planar(self, g):
        return nx.is_planar(g)

    def hamiltonian_path(self, g):
        # nx.is_tournament(g)
        return nx.tournament.hamiltonian_path(g)


if __name__ == "__main__":
    r = tk.Tk()
    app = App(r)
    app.run()
