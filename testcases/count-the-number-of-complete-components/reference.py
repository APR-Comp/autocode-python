from typing import List


class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
                # Helper function to check if a component is complete
        def is_complete(graph, component):
            vertices = len(component)
            edges = sum(len(graph[v]) for v in component) // 2
            return edges == vertices * (vertices - 1) // 2

        # Initialize graph
        graph = {i: [] for i in range(n)}
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        # Initialize visited set and count of complete components
        visited = set()
        complete_components = 0

        for vertex in range(n):
            if vertex not in visited:
                # Perform BFS to find all vertices in the current connected component
                queue = [vertex]
                visited.add(vertex)
                component = []
                while queue:
                    v = queue.pop(0)
                    component.append(v)
                    for neighbor in graph[v]:
                        if neighbor not in visited:
                            queue.append(neighbor)
                            visited.add(neighbor)

                # Check if the component is complete
                if is_complete(graph, component):
                    complete_components += 1

        return complete_components