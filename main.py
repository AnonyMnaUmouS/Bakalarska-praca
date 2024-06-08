import itertools
import time
import tkinter as tk
import random
import networkx as nx
from PIL import Image, ImageDraw, ImageFont
from itertools import combinations
from tkinter import messagebox, PhotoImage, filedialog, ttk
from tkinter import font as font
from math import comb


class App:
    def __init__(self, root):
        self.result = None
        self.button_back_to_load_id = None
        self.combo = None
        self.button_search_id = None
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

        self.width = self.root.winfo_screenwidth() - 50
        self.height = self.root.winfo_screenheight() - 100

        self.root.geometry(f"{self.width}x{self.height}")

        # self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#FFFFFF")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.start_screen()

        self.root.mainloop()

    def start_screen(self):
        self.canvas.delete('all')
        if self.nodes_label is not None:
            self.nodes_label.destroy()
        if self.edges_label is not None:
            self.edges_label.destroy()
        if self.enter_nodes is not None:
            self.enter_nodes.destroy()
        if self.enter_edges is not None:
            self.enter_edges.destroy()

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

    def button_click(self, event):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        else:
            self.graphs.parse(False, self.enter_nodes.get(), self.enter_edges.get("1.0", 'end-1c'))
            self.prepare_to_draw(False)

    def button_click_token(self, event):
        if self.enter_nodes.get() == "":
            messagebox.showinfo("Error", "Please enter nodes")
        else:
            def button_click_token(event1):
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

            img1 = PhotoImage(file='create_token_graph.png')
            self.canvas.create_image(20 + img1.width() / 2, 130, image=img1, tags="button")
            self.canvas.tag_bind("button", "<Button-1>", button_click_token)

            img2 = PhotoImage(file='back.png')
            self.button_back_id = self.canvas.create_image(self.width - img2.width() / 2,
                                                           self.height - img2.height() / 2,
                                                           image=img2, tags="button_back")
            self.canvas.tag_bind(self.button_back_id, "<Button-1>", self.button_back)

            self.root.mainloop()

    def button_back_to_load(self, event):
        self.start_screen()

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
        if self.result is not None:
            self.result.destroy()

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

        img2 = PhotoImage(file='save_picture.png')
        self.button_save_id = self.canvas.create_image(self.width - img1.width() - img2.width() / 2,
                                                       self.height - img2.height() / 2, image=img2, tags="button_save")
        self.canvas.tag_bind(self.button_save_id, "<Button-1>", self.button_save)

        img3 = PhotoImage(file='save_graph.png')
        self.button_save_graph_id = self.canvas.create_image(
            self.width - img1.width() - img2.width() - img3.width() / 2,
            self.height - img3.height() / 2, image=img3,
            tags="button_save_graph")
        self.canvas.tag_bind(self.button_save_graph_id, "<Button-1>", self.button_save_graph)

        img4 = PhotoImage(file='search.png')
        self.button_search_id = self.canvas.create_image(
            self.width - img4.width() / 2,
            self.height - img3.height() - img4.height() / 2, image=img4,
            tags="button_search")
        self.canvas.tag_bind(self.button_search_id, "<Button-1>", self.button_search)

        self.combo = ttk.Combobox(
            state="readonly",
            values=["Coloring", "Node connectivity", "Edge connectivity", "Regular", "Eulerian path", "Eulerian cycle",
                    "Complete graph", "Tree", "Planar", "Girth", "Johnson graph", "Hamiltonian graph"]  # Shortest path, Hamiltonian
        )
        self.combo.place(x=self.width - img4.width() - 150, y=self.height - 100)

        self.root.mainloop()

    def draw_algorithm(self, nodes, edges, colors_dict=None):

        for edge in edges:
            x = self.graphs.positions[self.graphs.nodes.index(edge[0])]
            y = self.graphs.positions[self.graphs.nodes.index(edge[1])]
            self.canvas.create_line(x[0], x[1], y[0], y[1], fill="red")

            self.canvas.create_oval(x[0] - 15, x[1] - 15, x[0] + 15, x[1] + 15, fill="#50a5fa", outline="")
            self.canvas.create_text(x[0], x[1], text=str(edge[0]), font=("Arial", 12), fill="black")

            self.canvas.create_oval(y[0] - 15, y[1] - 15, y[0] + 15, y[1] + 15, fill="#50a5fa", outline="")
            self.canvas.create_text(y[0], y[1], text=str(edge[1]), font=("Arial", 12), fill="black")

        for i in range(len(nodes)):
            pos = self.graphs.positions[self.graphs.nodes.index(nodes[i])]
            self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill="#F47361", outline="")
            self.canvas.create_text(pos[0], pos[1], text=str(nodes[i]), font=("Arial", 12), fill="black")

        if colors_dict is not None:
            colors = {}
            if max(colors_dict.values())+1 > 6:
                for i in range(max(colors_dict.values())+1):
                    colors[i] = f'#{random.randint(0, 0xFFFFFF):06x}'
            else:
                colors = {0: "red", 1: "green", 2: "blue", 3: "yellow", 4: "orange", 5: "purple"}

            for key, value in colors_dict.items():
                pos = self.graphs.positions[self.graphs.nodes.index(key)]
                self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill=colors[value],
                                        outline="")
                self.canvas.create_text(pos[0], pos[1], text=str(key), font=("Arial", 12), fill="black")

    def draw(self):
        for item in self.canvas.find_all():
            if item not in [self.button_back_id, self.button_save_id, self.button_save_graph_id, self.button_search_id]:
                self.canvas.delete(item)

        for x, y in self.graphs.edges:
            x = self.graphs.positions[self.graphs.nodes.index(x)]
            y = self.graphs.positions[self.graphs.nodes.index(y)]
            self.canvas.create_line(x[0], x[1], y[0], y[1], fill="black")

        for i in range(len(self.graphs.nodes)):
            pos = self.graphs.positions[i]
            self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill="#50a5fa", outline="")
            self.canvas.create_text(pos[0], pos[1], text=str(self.graphs.nodes[i].strip("(").strip(")")), font=("Arial", 12), fill="black")

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
                    color = self.canvas.itemcget(item, "fill")
                    draw.line([(x1, y1), (x2, y2)], fill=color)
                elif item_type == "oval":
                    x1, y1, x2, y2 = self.canvas.coords(item)
                    draw.ellipse([(x1, y1), (x2, y2)], fill=self.canvas.itemcget(item, "fill"))
                elif item_type == "text":
                    x, y = self.canvas.coords(item)
                    text = self.canvas.itemcget(item, "text")
                    text_color = self.canvas.itemcget(item, "fill")
                    draw.text((x, y), text, fill=text_color, font=font)

            # Save the PIL Image as a PNG file
            img.save(filename, "PNG")
            messagebox.showinfo("Success", "Image saved successfully!")

    def button_search(self, event):
        graph = self.graphs.token if self.graphs.token.nodes else self.graphs.g
        text = ""

        self.draw()

        if self.result is not None:
            self.result.destroy()
        if self.combo.get() == "Johnson graph":
            flag = self.graphs.is_johnson_graph(graph)
            if flag:
                text = "Graph is Johnson Graph."
            else:
                text = "Graph is not Johnson Graph."
        elif self.combo.get() == "Regular":
            flag = self.graphs.is_regular(graph)
            if flag:
                text = "Graph is regular."
            else:
                text = "Graph is not regular."
        elif self.combo.get() == "Eulerian path":
            flag = self.graphs.has_eulerian_path(graph)
            if flag:
                # text = f'There is eulerian path:\n{list(nx.eulerian_path(graph))}'
                text = "Graph has eulerian path."
            else:
                text = "Graph has no eulerian path."
        elif self.combo.get() == "Eulerian cycle":
            flag = self.graphs.has_eulerian_cycle(graph)
            if flag:
                # text = f'There is eulerian cycle:\n{list(nx.eulerian_circuit(graph))}'
                text = "Graph has eulerian cycle."
            else:
                text = "Graph has no eulerian cycle."
        elif self.combo.get() == "Hamiltonian graph":
            flag = self.graphs.has_hamiltonian_path(graph)
            if flag:
                text = "Graph has hamiltonian path."
            else:
                text = "Graph has no hamiltonian path."
        elif self.combo.get() == "Complete graph":
            flag = self.graphs.is_complete(graph)
            if flag:
                text = "Graph is complete."
            else:
                text = "Graph is not complete."
        elif self.combo.get() == "Tree":
            flag = self.graphs.is_tree(graph)
            if flag:
                text = "Graph is tree."
            else:
                text = "Graph is not tree."
        elif self.combo.get() == "Planar":
            flag = self.graphs.is_planar(graph)
            if flag:
                text = "Graph is planar."
            else:
                text = "Graph is not planar."

        elif self.combo.get() == "Girth":
            number = self.graphs.girth(graph)
            nodes = ""
            for lst in nx.cycle_basis(graph):
                if len(lst) == number:
                    nodes = lst
                    break
            edges = []

            for i in range(len(nodes) - 1):
                edges.append((nodes[i], nodes[i+1]))
            edges.append((nodes[-1], nodes[0]))

            text = f'Girth has length number {number}.'
            self.draw_algorithm(nodes, edges)

        elif self.combo.get() == "Coloring":
            number = self.graphs.coloring(graph)
            colors = nx.coloring.greedy_color(graph, strategy="largest_first")
            text = f'Graph has chromatic number {number}.'
            self.draw_algorithm("", "", colors)

        elif self.combo.get() == "Node connectivity":
            number = self.graphs.node_connectivity(graph)
            nodes = list(nx.minimum_node_cut(graph))
            text = f'{number} nodes to make graph unconnected.'
            self.draw_algorithm(nodes, "")

        elif self.combo.get() == "Edge connectivity":
            number = self.graphs.edge_connectivity(graph)
            edges = list(nx.minimum_edge_cut(graph))
            text = f'{number} edges to make graph unconnected.'
            self.draw_algorithm("", edges)

        if text != "":
            custom_font = ('Arial', 12)
            text_width = font.Font(font=custom_font).measure(text.split("\n")[0])
            self.result = tk.Label(font=custom_font, text=text)
            x_position = self.width - text_width - 20
            y_position = self.height - 165
            self.result.place(x=x_position, y=y_position)

            # custom_font = ('Arial', 12)
            # text_width = font.Font(font=custom_font).measure(text.split("\n")[0])
            # self.result = tk.Label(font=custom_font, text=text)
            # self.result.place(x=self.width - text_width - 20, y=self.height - 165)

    def button_save_graph(self, event):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("TXT files", "*.txt"), ("All files", "*.*")],
                                                title="Save the graph as...")

        if filename:
            if self.graphs.token.nodes:
                graph = self.graphs.token
            else:
                graph = self.graphs.g
            with open(filename, 'w') as file:
                file.write(', '.join(map(str, graph.nodes)) + '\n')
                file.write(', '.join(f"({a}, {b})" for a, b in graph.edges) + '\n')

                messagebox.showinfo("Success", "Graph saved successfully!")

    def button_back(self, event):
        if self.result is not None:
            self.result.destroy()

        self.new_graph(event, ', '.join(map(str, self.graphs.g.nodes)),
                       ', '.join(f"({a}, {b})" for a, b in self.graphs.g.edges))

    def new_graph(self, a, nodes="", edges=""):
        self.graphs.nodes = []
        self.graphs.edges = []
        self.graphs.positions = []

        self.canvas.delete('all')
        if self.combo is not None:
            self.combo.destroy()
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

        img3 = PhotoImage(file='back.png')
        self.button_back_to_load_id = self.canvas.create_image(self.width - img3.width() / 2,
                                                               self.height - img3.height() / 2,
                                                               image=img3, tags="button_back_to_load")
        self.canvas.tag_bind(self.button_back_to_load_id, "<Button-1>", self.button_back_to_load)

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

    # def run(self):
    #     self.root.mainloop()


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

        if "(" in nodes:
            node = ""
            for char in nodes:
                if char == '(':
                    node = ""
                elif char == ')':
                    vertex = [item.strip() for item in node.replace("'", "").split(",")]
                    result = ", ".join(vertex)
                    self.g.add_node("(" + result + ")")
                else:
                    node += char

            # ((1, 2), (1, 3)), ((1, 2), (2, 3)), ((1, 3), (2, 3))
            stack = []
            stack_of_nodes = []

            for char in edges:
                if char != ")":
                    stack.append(char)
                else:
                    node = ""
                    while stack and stack[-1] != "(":
                        node = stack.pop() + node
                    if node != "":
                        stack_of_nodes.append("(" + node + ")")
            for i in range(len(stack_of_nodes)//2):
                self.g.add_edge(stack_of_nodes[i*2], stack_of_nodes[i*2+1])

        else:
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
        node_combinations = [f"({', '.join(node)})" for node in node_combinations]
        self.token.add_nodes_from(node_combinations)

        for nodes1 in self.token.nodes:
            for nodes2 in self.token.nodes:
                # n1 = set(nodes1.strip("(").strip(")").split(", "))
                # n2 = set(nodes2.strip("(").strip(")").split(", "))
                n1 = set(nodes1.replace("(", "").replace(")", "").split(", "))
                n2 = set(nodes2.replace("(", "").replace(")", "").split(", "))
                print("n1, n2", n1, n2)
                if n1 != n2 and len(n1.intersection(n2)) == k - 1:
                    diff = n1 ^ n2
                    print("diff:", diff)
                    if self.g.has_edge(diff.pop(), diff.pop()):
                        self.token.add_edge(nodes1, nodes2)

        print("nodes:", self.token.nodes)
        print("edges:", self.token.edges)

    def girth(self, g):
        # print(nx.cycle_basis(g))
        return nx.girth(g)

    def shortest_path(self, g):
        return nx.shortest_path(g, source=1, target=6)

    def is_planar(self, g):
        return nx.is_planar(g)

    def is_tree(self, g):
        return nx.is_tree(g)

    def is_complete(self, g):
        # complete_graph = nx.complete_graph(len(g.nodes))
        # return nx.is_isomorphic(g, complete_graph)
        if not self.is_regular(g):
            return False
        return True if g.degree(list(g.nodes)[0]) == len(g.nodes) - 1 else False

    def is_regular(self, g):
        return nx.is_regular(g)

    def edge_connectivity(self, g):
        # print(nx.minimum_edge_cut(g))
        return nx.edge_connectivity(g)

    def node_connectivity(self, g):
        # print(graph.node_connectivity(graph.g))
        return nx.node_connectivity(g)

    def coloring(self, g):
        return max(nx.coloring.greedy_color(g, strategy="largest_first").values()) + 1

    # def is_eulerian(self, g):
    #     return nx.is_eulerian(g)

    def has_eulerian_cycle(self, g):
        return nx.is_eulerian(g) and len(list(nx.eulerian_circuit(g))) == len(g.edges())

    def has_eulerian_path(self, g):
        return nx.has_eulerian_path(g)

    def has_hamiltonian_path(self, graph):
        n = len(graph.nodes)

        for start_node in graph.nodes:
            stack = [(start_node, [start_node], {start_node})]

            while stack:
                current_node, path, visited = stack.pop()

                if len(path) == n:
                    return True

                for neighbor in graph.neighbors(current_node):
                    if neighbor not in visited:
                        new_visited = visited.copy()
                        new_visited.add(neighbor)
                        new_path = path + [neighbor]
                        stack.append((neighbor, new_path, new_visited))

        return False
        # def backtrack(current_node, visited, path):
        #     if len(path) == len(graph):
        #         return True
        #
        #     for neighbor in graph.neighbors(current_node):
        #         if neighbor not in visited:
        #             visited.add(neighbor)
        #             path.append(neighbor)
        #
        #             if backtrack(neighbor, visited, path):
        #                 return True
        #
        #             # Backtrack
        #             visited.remove(neighbor)
        #             path.pop()
        #
        #     return False
        #
        # for start_node in graph.nodes:
        #     visited = {start_node}
        #     path = [start_node]
        #
        #     if backtrack(start_node, visited, path):
        #         return True
        #
        # return False
        # nodes = g.nodes
        # edges = g.edges
        #
        # g = nx.DiGraph()
        # g.add_nodes_from(nodes)
        #
        # for edge in edges:
        #     g.add_edge(edge[0], edge[1])
        #     g.add_edge(edge[1], edge[0])
        #
        # # if not nx.is_tournament(g):
        # #     return False
        # print(list(nx.tournament.hamiltonian_path(g)))
        # return False if nx.tournament.hamiltonian_path(g) == [] else True

    def is_johnson_graph(self, g):
        # if g == self.g:
        #     return False
        n = len(self.g.nodes)
        if not self.token.nodes:
            m = len(list(self.g.nodes)[0])
        else:
            m = len(list(self.token.nodes)[0])

        if m == 1:
            if self.is_complete(g):
                return True
            return False

        if m > n / 2:
            return False

        expected_nodes = set(combinations(self.g.nodes, m))
        if set(g.nodes) != expected_nodes:
            return False

        for u, v in g.edges:
            if len(set(u).intersection(set(v))) != m - 1:
                return False

        for u in g.nodes:
            for v in g.nodes:
                if u != v and len(set(u).intersection(set(v))) == m - 1:
                    if not g.has_edge(u, v):
                        return False

        return True


if __name__ == "__main__":
    r = tk.Tk()
    app = App(r)





