import React, { useEffect } from 'react';
import styles from './ToastMessage.module.css';

interface ToastProps {
  message: string;
  onClose?: () => void;
  duration?: number; // ms
}

export default function ToastMessage({ message, onClose, duration = 3000 }: ToastProps) {
  useEffect(() => {
    const t = setTimeout(() => onClose && onClose(), duration);
    return () => clearTimeout(t);
  }, [duration, onClose]);

  return (
    <div className={styles.toastContainer} role="status" aria-live="polite">
      <div className={styles.toastBody}>{message}</div>
      <button className={styles.toastClose} onClick={() => onClose && onClose()} aria-label="Close">×</button>
    </div>
  );
}
