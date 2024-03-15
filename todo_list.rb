class TodoList
  attr_accessor :tasks

  def initialize
    @tasks = []
  end

  def add_task(task)
    @tasks << task
    puts "Task '#{task}' added to the list at position #{@tasks.length}."
  end

  def view_tasks
    if @tasks.empty?
      puts "No tasks in the list."
    else
      puts "Tasks in the list:"
      @tasks.each_with_index do |task, index|
        puts "#{index + 1}. #{task}"
      end
    end
  end

  def complete_task(task_index)
    if task_index >= 0 && task_index < @tasks.length
      completed_task = @tasks.delete_at(task_index)
      puts "Task '#{completed_task}' marked as completed."
    else
      puts "Invalid task index."
    end
  end

  def remove_task(task_index)
    if task_index >= 0 && task_index < @tasks.length
      removed_task = @tasks.delete_at(task_index)
      puts "Task '#{removed_task}' removed from the list."
    else
      puts "Invalid task index."
    end
  end
end

def manage_todo_list(todo_list)
  loop do
    puts "\n--- To-Do List Manager ---"
    puts "1. Add Task"
    puts "2. View Tasks"
    puts "3. Complete Task"
    puts "4. Remove Task"
    puts "5. Exit"
    print "Enter your choice: "
    choice = gets.chomp.to_i

    case choice
    when 1
      print "Enter task: "
      task = gets.chomp
      todo_list.add_task(task)
    when 2
      todo_list.view_tasks
    when 3
      print "Enter task index to mark as completed: "
      index = gets.chomp.to_i - 1
      todo_list.complete_task(index)
    when 4
      print "Enter task index to remove: "
      index = gets.chomp.to_i - 1
      todo_list.remove_task(index)
    when 5
      puts "Exiting..."
      break
    else
      puts "Invalid choice. Please enter a number from 1 to 5."
    end
  end
end

todo_list = TodoList.new
manage_todo_list(todo_list)