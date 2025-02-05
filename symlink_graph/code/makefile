all: ../report/task_flow.png

include ../../generic.make

../output/graph.txt: graphmaker.sh | ../output
	sh graphmaker.sh
../report/task_flow.png: ../output/graph.txt | ../output ../report
	dot -Grankdir=LR -Tpng ../output/graph.txt -o ../report/task_flow.png
runorder: ../output/graph.txt | ../output # This topological sort of tasks could produce the root-level Makefile
	sed '1d; $$d' ../output/graph.txt | sed 's/->/ /' | tsort | sed 's/\(.*\)/make -C \1\/code/'