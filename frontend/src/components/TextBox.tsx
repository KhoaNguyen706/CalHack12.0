// src/components/TextBox.tsx
import React, { useState } from "react";

type TextBoxProps = {
  label?: string;
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  className?: string;
};

export default function TextBox({
  label,
  placeholder = "Enter text...",
  value = "",
  onChange,
  className = "",
}: TextBoxProps) {
  const [text, setText] = useState(value);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value);
    if (onChange) onChange(e.target.value);
  };

  return (
    <div className={`flex flex-col ${className}`}>
      {label && <label className="mb-1 font-medium text-gray-700">{label}</label>}
      <input
        type="text"
        value={text}
        onChange={handleChange}
        placeholder={placeholder}
        className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
}
