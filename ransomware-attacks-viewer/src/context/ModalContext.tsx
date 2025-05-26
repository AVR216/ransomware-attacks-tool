import { createContext, useState, ReactNode } from "react";

interface ModalContextType {
  isOpen: boolean;
  countryCode: string | null;
  openModal: (code: string) => void;
  closeModal: () => void;
}

export const ModalContext = createContext<ModalContextType>({
  isOpen: false,
  countryCode: null,
  openModal: () => {},
  closeModal: () => {},
});

export const ModalProvider = ({ children }: { children: ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [countryCode, setCountryCode] = useState<string | null>(null);

  const openModal = (code: string) => {
    setCountryCode(code);
    setIsOpen(true);
  };

  const closeModal = () => {
    setIsOpen(false);
    setCountryCode(null);
  };

  return (
    <ModalContext.Provider value={{ isOpen, countryCode, openModal, closeModal }}>
      {children}
    </ModalContext.Provider>
  );
};
