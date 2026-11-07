"""
Matrix Graph Architecture (3D+1D)
==================================
3-layer 3D graph: Luar (0-9-0) <-> Magic Square (gateway) <-> Dalam (0-19-0)
+ Vortex Rings + Infinity Portal (digital root)
+ 3D space (i,j,k) + 1D time (ring traversal)

This is the structural core of the Guardian pipeline: Stage 0 (ROOT) and
Stages 1-9 (Luar/mod-10) / 10-19 (Dalam/mod-20) in
guardian.pipeline.stages.Stage map directly onto the 'luar' and 'dalam'
layers built here.

2D variant: (i+j)%modulus with same layering
"""


class Node:
    def __init__(self, name: str, node_type: str, layer: str, value=None, pos=None):
        self.name = name
        self.type = node_type  # 'grid', 'value', 'core', 'infinity'
        self.layer = layer    # 'luar', 'ms', 'dalam'
        self.value = value
        self.pos = pos        # (i,j,k) for grid, None for value/core
        self.edges = set()

    def connect(self, other: 'Node'):
        self.edges.add(other)
        other.edges.add(self)

    def __repr__(self):
        return f"{self.layer}:{self.name}={self.value}"


class MatrixGraph:
    def __init__(self, size=11):
        self.size = size
        self.nodes = {}  # name -> Node
        self.layers = {'luar': {}, 'ms': {}, 'dalam': {}}

    def _name(self, layer, ntype, key):
        return f"{layer}_{ntype}_{key}"

    # --- 3D Layer Builder ---

    def _build_layer(self, layer, modulus):
        """Build 3D grid + value + core + rings for a layer.
        Grid: (i,j,k) for i,j,k in 0..size-1
        Formula: (i+j+k) % modulus
        Rings: diag (i,i,i), anti (i,size-1-i,i)
        """
        ms = self.nodes
        S = self.size

        def get_val(i, j, k):
            return (i + j + k) % modulus

        # -- 3D Grid nodes --
        for i in range(S):
            for j in range(S):
                for k in range(S):
                    val = get_val(i, j, k)
                    n = Node(self._name(layer, 'grid', f'{i}-{j}-{k}'), 'grid', layer, val, (i, j, k))
                    ms[n.name] = n

        # -- Value nodes --
        unique_vals = sorted(set(get_val(i, j, k) for i in range(S) for j in range(S) for k in range(S)))
        for v in unique_vals:
            n = Node(self._name(layer, 'value', str(v)), 'value', layer, v)
            ms[n.name] = n

        # -- Grid -> Value edges --
        for i in range(S):
            for j in range(S):
                for k in range(S):
                    val = get_val(i, j, k)
                    g = ms[self._name(layer, 'grid', f'{i}-{j}-{k}')]
                    v = ms[self._name(layer, 'value', str(val))]
                    g.connect(v)

        # -- Diag Ring (i,i,i) CW --
        for t in range(S):
            i1 = j1 = k1 = t
            i2 = j2 = k2 = (t + 1) % S
            g1 = ms[self._name(layer, 'grid', f'{i1}-{j1}-{k1}')]
            g2 = ms[self._name(layer, 'grid', f'{i2}-{j2}-{k2}')]
            g1.connect(g2)

        # -- Anti Ring (i,size-1-i,i) CCW --
        for t in range(S):
            i1, j1, k1 = t, S - 1 - t, t
            i2 = (t + 1) % S
            j2 = S - 1 - (t + 1) % S
            k2 = (t + 1) % S
            g1 = ms[self._name(layer, 'grid', f'{i1}-{j1}-{k1}')]
            g2 = ms[self._name(layer, 'grid', f'{i2}-{j2}-{k2}')]
            g1.connect(g2)

        # -- Core (center of 3D) --
        core_val = 0
        core = Node(self._name(layer, 'core', '0'), 'core', layer, core_val)
        ms[core.name] = core
        cx = S // 2
        grid_core = ms[self._name(layer, 'grid', f'{cx}-{cx}-{cx}')]
        core.connect(grid_core)

        v0 = ms[self._name(layer, 'value', '0')]
        core.connect(v0)

    # --- Magic Square (2D slice at z=5) ---

    def _build_magic_square(self):
        ms = self.nodes
        layer = 'ms'
        K = 5  # z-coordinate of magic square plane

        ms_data = [
            [8, 1, 6],
            [3, 5, 7],
            [4, 9, 2]
        ]
        constant = 15

        # -- Grid nodes (z=5 plane) --
        for i in range(3):
            for j in range(3):
                val = ms_data[i][j]
                gi, gj = i + 4, j + 4
                n = Node(self._name(layer, 'grid', f'{i}-{j}'), 'grid', layer, val, (gi, gj, K))
                ms[n.name] = n

        # -- Value nodes --
        for v in [1, 2, 3, 4, 5, 6, 7, 8, 9, 15]:
            n = Node(self._name(layer, 'value', str(v)), 'value', layer, v)
            ms[n.name] = n

        # Grid -> Value
        for i in range(3):
            for j in range(3):
                val = ms_data[i][j]
                g = ms[self._name(layer, 'grid', f'{i}-{j}')]
                v = ms[self._name(layer, 'value', str(val))]
                g.connect(v)

        # Diag Ring (grid): 8->5->2->8
        diag = [(0, 0), (1, 1), (2, 2)]
        for k in range(3):
            i1, j1 = diag[k]
            i2, j2 = diag[(k + 1) % 3]
            g1 = ms[self._name(layer, 'grid', f'{i1}-{j1}')]
            g2 = ms[self._name(layer, 'grid', f'{i2}-{j2}')]
            g1.connect(g2)

        # Anti Ring (grid): 4->5->6->4
        anti = [(2, 0), (1, 1), (0, 2)]
        for k in range(3):
            i1, j1 = anti[k]
            i2, j2 = anti[(k + 1) % 3]
            g1 = ms[self._name(layer, 'grid', f'{i1}-{j1}')]
            g2 = ms[self._name(layer, 'grid', f'{i2}-{j2}')]
            g1.connect(g2)

        # Vortex Fisik Ring (value): 1->2->4->8->7->5->1
        fisik = [1, 2, 4, 8, 7, 5]
        for k in range(6):
            v1 = ms[self._name(layer, 'value', str(fisik[k]))]
            v2 = ms[self._name(layer, 'value', str(fisik[(k + 1) % 6]))]
            v1.connect(v2)

        # Vortex Tinggi Ring (value): 3->6->9->3
        tinggi = [3, 6, 9]
        for k in range(3):
            v1 = ms[self._name(layer, 'value', str(tinggi[k]))]
            v2 = ms[self._name(layer, 'value', str(tinggi[(k + 1) % 3]))]
            v1.connect(v2)

        # Core
        core = Node(self._name(layer, 'core', '5'), 'core', layer, 5, (5, 5, 5))
        ms[core.name] = core
        grid_core = ms[self._name(layer, 'grid', '1-1')]
        core.connect(grid_core)

        v5 = ms[self._name(layer, 'value', '5')]
        core.connect(v5)

        # -- Infinity portal (digital root spokes) --
        inf = Node('infinity_root', 'infinity', 'ms', None)
        ms[inf.name] = inf
        for v in [1, 2, 3, 4, 5, 6, 7, 8, 9, 15]:
            val_node = ms[self._name(layer, 'value', str(v))]
            if v == 15:
                val_node.connect(inf)
                continue

            # Spoke: root -> root+9 -> root+18 -> ... -> infinity_root
            prev = val_node
            for step in range(1, 7):
                nv = v + step * 9
                nn = Node(self._name(layer, 'infinity', f'{v}_{nv}'), 'infinity', layer, nv)
                ms[nn.name] = nn
                prev.connect(nn)
                prev = nn
            prev.connect(inf)

        return constant

    # --- Cross-Layer Edges (through z=5 plane) ---

    def _build_cross_layer(self):
        ms = self.nodes
        K = 5  # magic square plane

        # Luar(i,j,5) <-> MS(i,j) <-> Dalam(i,j,5)
        for i in range(3):
            for j in range(3):
                gi, gj = i + 4, j + 4
                luar_grid = ms[self._name('luar', 'grid', f'{gi}-{gj}-{K}')]
                ms_grid = ms[self._name('ms', 'grid', f'{i}-{j}')]
                dalam_grid = ms[self._name('dalam', 'grid', f'{gi}-{gj}-{K}')]
                luar_grid.connect(ms_grid)
                ms_grid.connect(dalam_grid)

        # Core connections
        luar_core = ms[self._name('luar', 'core', '0')]
        ms_core = ms[self._name('ms', 'core', '5')]
        dalam_core = ms[self._name('dalam', 'core', '0')]
        luar_core.connect(ms_core)
        ms_core.connect(dalam_core)

    # --- Infinity Series ---

    def digital_root(self, n):
        if n == 0:
            return 0
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    def infinity_series(self, root_val, count=10):
        series = []
        x = root_val
        while len(series) < count:
            series.append(x)
            x += 9
        return series

    # --- Build ---

    def build(self):
        """Build the full 3-layer 3D graph."""
        self._build_layer('luar', 10)    # 0-9-0
        self._build_layer('dalam', 20)   # 0-19-0
        self._build_magic_square()
        self._build_cross_layer()
        return self

    # --- Queries ---

    def get_node(self, name):
        return self.nodes.get(name)

    def get_layer_nodes(self, layer):
        return [n for n in self.nodes.values() if n.layer == layer]

    def get_layer_counts(self):
        return {
            'luar': len([n for n in self.nodes.values() if n.layer == 'luar']),
            'ms': len([n for n in self.nodes.values() if n.layer == 'ms']),
            'dalam': len([n for n in self.nodes.values() if n.layer == 'dalam']),
            'total': len(self.nodes)
        }

    def get_edge_counts(self):
        edge_set = set()
        for n in self.nodes.values():
            for e in n.edges:
                edge_set.add(tuple(sorted((n.name, e.name))))
        return len(edge_set)

    def print_summary(self):
        counts = self.get_layer_counts()
        edges = self.get_edge_counts()
        print("=" * 50)
        print("  MATRIX GRAPH ARCHITECTURE (3D+1D)")
        print("=" * 50)
        print(f"  Size: {self.size}x{self.size}x{self.size}")
        for layer, count in counts.items():
            if layer != 'total':
                print(f"  Layer {layer}: {count} nodes")
        print(f"  Total nodes: {counts['total']}")
        print(f"  Total edges: {edges}")
        print()

    def print_infinity_series(self):
        print("INFINITY PORTAL (Digital Root Series):")
        print("-" * 40)
        for root in range(1, 10):
            series = self.infinity_series(root, 6)
            print(f"  Jalur {root}: {' -> '.join(str(x) for x in series)} -> inf")
        print(f"  0 (core): 0 (tidak tereduksi)")
        print()

    def print_vortex_rings(self):
        print("VORTEX RINGS:")
        print("-" * 40)
        fisik = [1, 2, 4, 8, 7, 5]
        print(f"  Fisik: {' -> '.join(str(x) for x in fisik)} -> 1")
        tinggi = [3, 6, 9]
        print(f"  Tinggi: {' -> '.join(str(x) for x in tinggi)} -> 3")
        print()

    def print_magic_square(self):
        print("MAGIC SQUARE 3x3 (z=5):")
        print("-" * 40)
        ms_data = [[8, 1, 6], [3, 5, 7], [4, 9, 2]]
        for row in ms_data:
            print(f"  {row[0]}  {row[1]}  {row[2]}")
        print(f"  Magic constant: 15")
        print(f"  Core: 5")
        print()

    def print_3d_sample(self, layer, z=5):
        """Print a 2D slice of a 3D layer at given z."""
        print(f"3D SLICE -- {layer.upper()} at z={z}:")
        print("-" * 40)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                n = self.get_node(f"{layer}_grid_{i}-{j}-{z}")
                if n:
                    row.append(str(n.value))
                else:
                    row.append('X')
            print(f"  {'  '.join(row)}")
        print()
