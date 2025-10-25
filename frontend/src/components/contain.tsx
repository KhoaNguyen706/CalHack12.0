import React from "react";

type ContainerProps = {
  children: React.ReactNode; // anything nested inside the container
};

export default function Container({ children }: ContainerProps) {
  return (
    <div className="max-w-5xl mx-auto px-4 py-8 bg-gray-100 rounded-lg shadow">
      {children}
    </div>
  );
}
