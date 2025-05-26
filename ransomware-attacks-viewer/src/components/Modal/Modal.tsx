import { ReactNode, useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import { useModalContext } from "../../hooks";

interface ModalProps { children: ReactNode }

export const Modal = ({ children }: ModalProps) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const { isOpen, closeModal } = useModalContext();
  const modalRoot = document.getElementById("modal");
  const eventListener = "keydown";

  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => e.key === "Escape" && closeModal();
    if (isOpen) document.addEventListener(eventListener, onEsc);
    return () => document.removeEventListener(eventListener, onEsc);
  }, [isOpen, closeModal]);

  if (!isOpen || !modalRoot) return null;

  return createPortal(
    <div
      className="fixed inset-0 flex items-center justify-center z-50"
    >
      <div
        ref={modalRef}
        onClick={e => e.stopPropagation()}
        className="
          relative
          bg-white dark:bg-gray-800
          rounded-2xl
          shadow-2xl
          p-6
          w-full max-w-lg
          mx-4
          transform transition-transform duration-300
          scale-100
        "
      >
        {children}

        <button
          onClick={closeModal}
          aria-label="Close modal"
          className="
            absolute top-4 right-4 
            text-gray-500 dark:text-gray-400 
            hover:text-gray-700 dark:hover:text-gray-200 
            focus:outline-none
          "
        >
          &times;
        </button>
      </div>
    </div>,
    modalRoot
  );
};
