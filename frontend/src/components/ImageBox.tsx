import React from "react";

type ImageBoxProps = {
  src: string;       // Image URL or path in /public
  alt: string;       // Alternative text
  width?: number | string;
  height?: number | string;
  className?: string;
};

export default function ImageBox({
  src,
  alt,
  width = "300px",
  height = "200px",
  className = "",
}: ImageBoxProps) {
  return (
    <div className={`overflow-hidden rounded-lg shadow-lg ${className}`}>
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        className="object-cover w-full h-full"
      />
    </div>
  );
}
