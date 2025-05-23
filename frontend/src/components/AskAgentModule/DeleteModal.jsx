import React from "react";

const DeleteModal = ({ confirmDeleteId, setConfirmDeleteId, deleteChat }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50 transition-opacity animate-fadeIn">
      <div className="bg-white p-6 rounded shadow-lg w-[90%] max-w-sm transform transition-all scale-95 animate-scaleIn">
        <h3 className="text-lg font-semibold mb-4">Confirm Delete</h3>
        <p className="text-sm text-gray-700 mb-6">
          Are you sure you want to delete this chat?
        </p>
        <div className="flex justify-end gap-4">
          <button
            onClick={() => setConfirmDeleteId(null)}
            className="text-gray-500 hover:underline text-sm"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              deleteChat(confirmDeleteId);
              setConfirmDeleteId(null);
            }}
            className="bg-red-600 text-white px-4 py-2 rounded text-sm hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteModal;
