git initizlize
#task 2 
1.mkdir test_folder
#I create a  folder named "test_folder"
2.touch test_folder/test.txt
#I  create a file named"test.txt" in the test_folder
3.echo "ROS LEARNING TASK" > test_folder/test.txt 
#I write some words in the test.txt
4.cat test_folder/test.txt
#I can know all the things in the test.txt
4.rm -r test_folder 
#I delete this folder

#task 3
src/: Contains all ROS2 packages.This is where i write and store my code.
build/:Hold intermediate build files
install/:Contains the final built artifacts
log/:Stores build logs and test output.
why source install/setup.bash is needed?
modify my current shell's environment so that ROS2 can find my custom packages.
