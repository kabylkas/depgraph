dhry_all: dhry0 dhry1 dhry2 dhry3 dhry4 dhry5

crafty_all: c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 

clean:
	rm -r clean_graphs
	mkdir clean_graphs
	rm -r traversed_graphs
	mkdir traversed_graphs

dhry0:
	mkdir dhry_output/dhry0
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry0 0 1

dhry1:
	mkdir dhry_output/dhry1
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry1 1 2

dhry2:
	mkdir dhry_output/dhry2
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry2 2 3

dhry3:
	mkdir dhry_output/dhry3
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry3 3 4

dhry4:
	mkdir dhry_output/dhry4
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry4 4 5

dhry5:
	mkdir dhry_output/dhry5
	python graph_edges_splitted.py ./input/dhry_edges/list ./dhry_output/dhry5 5 6


c0:
	mkdir crafty_output/crafty0
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty0 0 176 

c1:
	mkdir crafty_output/crafty1
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty1 176 352

c2:
	mkdir crafty_output/crafty2
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty2 352 528

c3:
	mkdir crafty_output/crafty3
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty3 528 704

c4:
	mkdir crafty_output/crafty4
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty4 704 880

c5:
	mkdir crafty_output/crafty5
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty5 880 1056

c6:
	mkdir crafty_output/crafty6
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty6 1056 1232

c7:
	mkdir crafty_output/crafty7
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty7 1232 1408

c8:
	mkdir crafty_output/crafty8
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty8 1408 1584

c9:
	mkdir crafty_output/crafty9
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty9 1584 1760

c10:
	mkdir crafty_output/crafty10
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty10 1760 1936

c11:
	mkdir crafty_output/crafty11
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty11 1936 2112

c12:
	mkdir crafty_output/crafty12
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty12 2112 2288

c13:
	mkdir crafty_output/crafty13
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty13 2288 2464

c14:
	mkdir crafty_output/crafty14
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty14 2464 2640

c15:
	mkdir crafty_output/crafty15
	python graph_edges_splitted.py ../build/release/run/crafty_edge_dump/list ./crafty_output/crafty15 2640 2816

