import React from 'react';

const TaskPipelineVisualizer = ({ intent, tasks, result }) => {
  return (
    <div className="flex flex-col space-y-4 p-4 bg-gray-50 rounded-lg shadow-inner text-sm w-full">
      {/* Intent Section */}
      {intent && (
        <div className="bg-white p-3 rounded border-l-4 border-blue-500 shadow-sm">
          <h4 className="font-semibold text-gray-700 mb-1">识别意图</h4>
          <p className="text-gray-600">{intent}</p>
        </div>
      )}

      {/* Tasks Section */}
      {tasks && tasks.length > 0 && (
        <div className="bg-white p-3 rounded border-l-4 border-yellow-500 shadow-sm">
          <h4 className="font-semibold text-gray-700 mb-2">执行计划</h4>
          <ul className="space-y-3">
            {tasks.map((task, index) => (
              <li key={index} className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-yellow-100 text-yellow-600 flex items-center justify-center text-xs font-bold mr-3 mt-0.5">
                  {index + 1}
                </span>
                <div className="flex-1">
                  <p className="font-medium text-gray-800">{task.name || task.agent}</p>
                  <p className="text-xs text-gray-500 mt-1">{task.description || task.task}</p>
                  {task.status && (
                    <span className={`text-xs px-2 py-0.5 rounded-full mt-2 inline-block ${
                      task.status === 'completed' ? 'bg-green-100 text-green-700' :
                      task.status === 'in_progress' ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      {task.status === 'completed' ? '已完成' : task.status === 'in_progress' ? '执行中' : '等待中'}
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Result Section */}
      {result && (
        <div className="bg-white p-3 rounded border-l-4 border-green-500 shadow-sm">
          <h4 className="font-semibold text-gray-700 mb-1">最终结果</h4>
          <div className="text-gray-600 whitespace-pre-wrap">{result}</div>
        </div>
      )}
    </div>
  );
};

export default TaskPipelineVisualizer;
