import tkinter as tk
from tkinter import messagebox, Button, PhotoImage
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import combinations
from tkinter import messagebox, Button, PhotoImage, Label


class GraphApp:
    def __init__(self, root):
        self.button_back_id = None
        self.enter_edges = None
        self.edges_label = None
        self.enter_nodes = None
        self.nodes_label = None
        self.root = root
        self.root.title("Graph Application")

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.positions = []
        self.nodes = []  # To store node IDs and coordinates
        self.edges = []  # To store edge IDs

        img = PhotoImage(file='new_graph.png')
        self.canvas.create_image(200, 200, image=img, tags="image_button1")
        self.canvas.tag_bind("image_button1", "<Button-1>", self.new_graph)
        self.canvas.bind('<B1-Motion>', self.move)
        self.canvas.bind('<ButtonPress>', self.klik)

        self.root.mainloop()

    def klik(self, event):
        ...

    def move(self, event):
        index = -1
        for i in range(len(self.positions)):
            if abs(self.positions[i][0] - event.x) < 15 and abs(self.positions[i][1] - event.y) < 15:
                index = i
                break
        if index != -1:
            self.positions[index] = (event.x, event.y)
            self.draw()

    def button_click(self, a):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        elif self.enter_edges.get("1.0", 'end-1c') == "":
            messagebox.showinfo("Error", "Please enter edges")
        else:
            self.parse(False)

    def button_click_token(self, a):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        elif self.enter_edges.get("1.0", 'end-1c') == "":
            messagebox.showinfo("Error", "Please enter edges")
        else:
            self.parse(True)

    def parse(self, token):
        nodes = self.enter_nodes.get()
        edges = self.enter_edges.get("1.0", 'end-1c')

        self.canvas.delete('all')
        self.nodes_label.destroy()
        self.edges_label.destroy()
        self.enter_nodes.destroy()
        self.enter_edges.destroy()

        nodes = nodes.split(",")
        # for i in range(len(nodes)):
        #     nodes[i] = nodes[i]

        if "(" in edges:
            edges = edges[1:-1].replace('), ', '),').split('),(')
            edges = [tuple(map(str, t.replace(' ', '').split(','))) for t in edges]
            # print(edges)
        else:
            edges = edges.split()
            for i in range(len(edges)):
                edges[i] = edges[i].split(",")
                # edges[i][0] = edges[i][0]
                # edges[i][1] = edges[i][1]
                edges[i] = tuple(edges[i])

        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)

        # print(g.nodes)
        # print(g.edges)

        if token:
            g = self.to_token(g)

        self.prepare_to_draw(g)

    # def draw1(self):
    #     p = nx.spring_layout(g)
    #
    #     fig, ax = plt.subplots(figsize=(4, 4))
    #     nx.draw(g, p, ax=ax, with_labels=True, node_size=700, node_color='skyblue', font_size=12, font_weight='bold',
    #             width=2)
    #
    #     canvas = FigureCanvasTkAgg(fig, master=self.root)
    #     canvas.draw()
    #
    #     canvas.get_tk_widget().place(x=0, y=0)

    def prepare_to_draw(self, g):
        layout = nx.spring_layout(g, seed=42)
        self.nodes, self.edges, self.positions = [], [], []

        for node in g.nodes():
            x, y = layout[node]
            self.positions.append((x * 150 + 150, y * 150 + 150))
            self.nodes.append(node)

        self.edges = list(g.edges)

        self.draw()

        img = PhotoImage(file='back.png')
        self.button_back_id = self.canvas.create_image(400 - img.width() / 2, 400 - img.height() / 2,
                                                       image=img, tags="button_back")
        self.canvas.tag_bind(self.button_back_id, "<Button-1>", self.button_back)

        self.root.mainloop()

    def draw(self):

        for item in self.canvas.find_all():
            if item != self.button_back_id:
                self.canvas.delete(item)

        for x, y in self.edges:
            x = self.positions[self.nodes.index(x)]
            y = self.positions[self.nodes.index(y)]
            self.canvas.create_line(x[0], x[1], y[0], y[1])

        for i in range(len(self.nodes)):
            pos = self.positions[i]
            self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill="#50a5fa", outline="")
            self.canvas.create_text(pos[0], pos[1], text=str(self.nodes[i]), font=("Arial", 12), fill="black")

        # img = PhotoImage(file='back.png')
        # self.canvas.create_image(400 - img.width() / 2, 400 - img.height() / 2, image=img,
        #                          tags="button_back")
        # self.canvas.tag_bind("button_back", "<Button-1>", self.button_back)
        # self.root.mainloop()

    def button_back(self, event):
        self.new_graph(event, ', '.join(map(str, self.nodes)), ', '.join(f"({a}, {b})" for a, b in self.edges))

    def new_graph(self, a, nodes="", edges=""):
        # print(a)
        self.canvas.delete('all')
        custom_font = ('Arial', 12)
        self.nodes_label = tk.Label(font=custom_font, text='Enter nodes:')
        self.nodes_label.place(x=20, y=20)
        self.enter_nodes = tk.Entry(width=60)
        self.enter_nodes.insert(tk.END, nodes)
        self.enter_nodes.place(x=20, y=50)

        self.edges_label = tk.Label(font=custom_font, text='Enter edges:')
        self.edges_label.place(x=20, y=100)
        self.enter_edges = tk.Text(self.root, width=45, height=5)
        self.enter_edges.insert(tk.END, edges)
        self.enter_edges.place(x=20, y=130)

        # enter_edges = tk.Entry(width=60)
        # enter_edges.place(x=20, y=130)

        img1 = PhotoImage(file='create_graph.png')
        self.canvas.create_image(20 + img1.width() / 2, 230 + img1.height() / 2, image=img1, tags="button1")
        self.canvas.tag_bind("button1", "<Button-1>", self.button_click)

        img2 = PhotoImage(file='create_token_graph.png')
        self.canvas.create_image(20 + img1.width() + img2.width() / 2, 230 + img2.height() / 2, image=img2,
                                 tags="button2")
        self.canvas.tag_bind("button2", "<Button-1>", self.button_click_token)

        self.root.mainloop()

    # def load_graph(self):
    #     # You can implement loading graph data from a file here
    #     messagebox.showinfo("Load Graph", "Functionality to load graph is not implemented yet.")

    def to_token(self, g, k=2):
        node_combinations = list(combinations(g.nodes, k))
        token = nx.Graph()
        token.add_nodes_from(node_combinations)

        for nodes1 in token.nodes:
            for nodes2 in token.nodes:
                if nodes1 != nodes2 and len(set(nodes1).intersection(nodes2)) == k - 1:
                    diff = set(nodes1) ^ set(nodes2)
                    if g.has_edge(diff.pop(), diff.pop()):
                        token.add_edge(nodes1, nodes2)

        # print(len(list(token.edges)))
        # print(list(token.edges))

        return token

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    r = tk.Tk()
    app = GraphApp(r)
    app.run()

# print(list(combinations([1, 2, 3, 4, 5, 6], 3)))
#
# g1 = nx.Graph()
# g1.add_nodes_from([1, 2, 3, 4])
# g1.add_edges_from([(1, 2), (1, 2), (2, 1), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
#
# g2 = nx.Graph()
# g2.add_nodes_from([1, 2, 3, 4])
# g2.add_edges_from([(1, 2), (2, 3), (3, 4)])
#
# g3 = nx.Graph()
# g3.add_nodes_from([1, 2, 3, 4])
# g3.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])
#
# g4 = nx.Graph()
# g4.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
# g4.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)])
#
# g5 = nx.Graph()
# g5.add_nodes_from([1, 2, 3, 4, 5, 6])
# g5.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 6), (2, 3), (2, 4), (4, 5)])
#
#
# def to_token(g, k=2):
#     node_combinations = list(combinations(g.nodes, k))
#     token = nx.Graph()
#     token.add_nodes_from(node_combinations)
#
#     for nodes1 in token.nodes:
#         for nodes2 in token.nodes:
#             if nodes1 != nodes2 and len(set(nodes1).intersection(nodes2)) == k - 1:
#                 diff = set(nodes1) ^ set(nodes2)
#                 if g.has_edge(diff.pop(), diff.pop()):
#                     token.add_edge(nodes1, nodes2)
#
#     print(len(list(token.edges)))
#     print(list(token.edges))
#
#     draw(token)
#
#     return token
#
#
# def draw(g):
#     p = nx.spring_layout(g)
#     nx.draw(g, p, with_labels=True, node_size=700, node_color='skyblue', font_size=12, font_weight='bold', width=2)
#     plt.show()


# to_token(g1)
# to_token(g2)
# to_token(g3)
# to_token(g4)

# to_token(g1, 3)

# to_token(g5, 3)

# Záloha
# import networkx as nx
# import matplotlib.pyplot as plt
# from itertools import combinations
# import tkinter as tk
# from tkinter import messagebox, Button, PhotoImage, Label
#
#
# class GraphApp:
#     def __init__(self, root):
#         self.enter_edges = None
#         self.edges_label = None
#         self.enter_nodes = None
#         self.nodes_label = None
#         self.root = root
#         self.root.title("Graph Application")
#
#         self.canvas = tk.Canvas(self.root, width=400, height=400)
#         self.canvas.pack()
#
#         self.nodes = {}  # To store node IDs and coordinates
#         self.edges = []  # To store edge IDs
#
#         img = PhotoImage(file='C:\\Users\\Tima\\Desktop\\Bakalarka\\Práca\\new_graph.png')
#         self.canvas.create_image(200, 200, image=img, tags="image_button1")
#         self.canvas.tag_bind("image_button1", "<Button-1>", self.new_graph)
#
#         self.root.mainloop()
#
#     def button_click(self, a):
#         if self.enter_nodes.get() == "":
#             messagebox.showinfo("Error", "Please enter nodes")
#         elif self.enter_edges.get("1.0", 'end-1c') == "":
#             messagebox.showinfo("Error", "Please enter edges")
#         else:
#             self.parse()
#
#     def parse(self):
#         nodes = self.enter_nodes.get()
#         edges = self.enter_edges.get("1.0", 'end-1c')
#
#         self.canvas.delete('all')
#         self.nodes_label.destroy()
#         self.edges_label.destroy()
#         self.enter_nodes.destroy()
#         self.enter_edges.destroy()
#
#         # print(nodes)
#         # print(edges)
#
#         nodes = nodes.split(",")
#         for i in range(len(nodes)):
#             nodes[i] = int(nodes[i])
#
#         # print(nodes)
#
#         edges = edges.split()
#
#         for i in range(len(edges)):
#             edges[i] = edges[i].split(",")
#             edges[i][0] = int(edges[i][0])
#             edges[i][1] = int(edges[i][1])
#             edges[i] = tuple(edges[i])
#
#         # print(edges)
#
#         g = nx.Graph()
#         g.add_nodes_from(nodes)
#         g.add_edges_from(edges)
#
#         print(g.nodes)
#         print(g.edges)
#
#         self.draw(g)
#
#     def draw(self, g):
#         p = nx.spring_layout(g)
#         print(p.values())
#         nx.draw(g, p, with_labels=True, node_size=700, node_color='skyblue', font_size=12, font_weight='bold', width=2)
#         plt.show()
#
#     def new_graph(self, a):
#         print(a)
#         self.canvas.delete('all')
#         custom_font = ('Arial', 12)
#         self.nodes_label = tk.Label(font=custom_font, text='Enter nodes:')
#         self.nodes_label.place(x=20, y=20)
#         self.enter_nodes = tk.Entry(width=60)
#         self.enter_nodes.place(x=20, y=50)
#
#         self.edges_label = tk.Label(font=custom_font, text='Enter edges:')
#         self.edges_label.place(x=20, y=100)
#         self.enter_edges = tk.Text(self.root, width=45, height=5)
#         self.enter_edges.place(x=20, y=130)
#
#         # enter_edges = tk.Entry(width=60)
#         # enter_edges.place(x=20, y=130)
#
#         img1 = PhotoImage(file='C:\\Users\\Tima\\Desktop\\Bakalarka\\Práca\\create_graph.png')
#         self.canvas.create_image(20+img1.width()/2, 230+img1.height()/2, image=img1, tags="button1")
#         self.canvas.tag_bind("button1", "<Button-1>", self.button_click)
#
#         img2 = PhotoImage(file='C:\\Users\\Tima\\Desktop\\Bakalarka\\Práca\\create_token_graph.png')
#         self.canvas.create_image(20+img1.width()+img2.width()/2, 230+img2.height()/2, image=img2, tags="button2")
#         self.canvas.tag_bind("button2", "<Button-1>", self.button_click)
#
#         self.root.mainloop()
#
#     # def load_graph(self):
#     #     # You can implement loading graph data from a file here
#     #     messagebox.showinfo("Load Graph", "Functionality to load graph is not implemented yet.")
#
#     def quit_app(self):
#         if messagebox.askokcancel("Quit", "Do you really want to quit?"):
#             self.root.destroy()
#
#     def run(self):
#         self.root.mainloop()
#
