import React, { useState } from 'react';
import './App.css';

function App() {
    const [firstCatalog, setFirstCatalog] = useState([]); // Первый каталог
    const [secondCatalog, setSecondCatalog] = useState([]); // Второй каталог
    const [selectedBookIndex, setSelectedBookIndex] = useState(null); // Выбранная книга

    // Загрузка XML с помощью XMLHttpRequest
    const loadXML = () => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/data.xml', true); // Асинхронный запрос

        xhr.onload = () => {
            if (xhr.status === 200) {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xhr.responseText, 'text/xml');

                // Извлечение первого каталога
                const firstCatalogData = xmlDoc.getElementsByTagName('catalog')[0];
                const firstHead = firstCatalogData.getElementsByTagName('head')[0].textContent;
                const firstBooks = firstCatalogData.getElementsByTagName('book');

                const firstCatalogBooks = [];
                for (let i = 0; i < firstBooks.length; i++) {
                    const title = firstBooks[i].getElementsByTagName('title')[0].textContent;
                    const author = firstBooks[i].getElementsByTagName('author')[0].textContent;
                    const year = firstBooks[i].getElementsByTagName('year')[0].textContent;
                    const janre = firstBooks[i].getElementsByTagName('janre')[0].textContent;

                    firstCatalogBooks.push({ title, author, year, janre });
                }

                setFirstCatalog({ head: firstHead, books: firstCatalogBooks });

                // Извлечение второго каталога
                const secondCatalogData = xmlDoc.getElementsByTagName('catalog')[1];
                const secondHead = secondCatalogData.getElementsByTagName('head')[0].textContent;
                const secondBooks = secondCatalogData.getElementsByTagName('book');

                const secondCatalogBooks = [];
                for (let i = 0; i < secondBooks.length; i++) {
                    const title = secondBooks[i].getElementsByTagName('title')[0].textContent;
                    const author = secondBooks[i].getElementsByTagName('author')[0].textContent;
                    const year = secondBooks[i].getElementsByTagName('year')[0].textContent;
                    const janre = secondBooks[i].getElementsByTagName('janre')[0].textContent;

                    secondCatalogBooks.push({ title, author, year, janre });
                }

                setSecondCatalog({ head: secondHead, books: secondCatalogBooks });
            } else {
                console.error('Ошибка при загрузке XML:', xhr.statusText);
            }
        };

        xhr.onerror = () => {
            console.error('Ошибка при выполнении запроса.');
        };

        xhr.send();
    };

    // Загружаем XML при монтировании компонента
    React.useEffect(() => {
        loadXML();
    }, []);

    // Обработчик изменения поля ввода
    const handleInputChange = (event) => {
        const index = parseInt(event.target.value, 10);
        if (!isNaN(index) && index >= 0) {
            setSelectedBookIndex(index);
        } else {
            setSelectedBookIndex(null);
        }
    };

    return (
        <div>
            {/* Поле ввода для выбора книги */}
            <div className="input-container">
                <input
                    type="number"
                    placeholder="Введите номер книги"
                    onChange={handleInputChange}
                    min="0"
                />
            </div>

            {/* Первый каталог */}
            {firstCatalog.head && (
                <div className="catalog-container">
                    <div className="catalog-head">{firstCatalog.head}</div>
                    <div className="books-container">
                        {firstCatalog.books.map((book, index) => (
                            <div
                                key={index}
                                className={`book ${selectedBookIndex === index ? 'selected' : ''}`}
                            >
                                <div className="book-title">{book.title}</div>
                                <div className="book-author">{book.author}</div>
                                <div className="book-year">{book.year}</div>
                                <div className="book-janre">{book.janre}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Второй каталог */}
            {secondCatalog.head && (
                <div className="catalog-container">
                    <div className="catalog-head">{secondCatalog.head}</div>
                    <div className="books-container">
                        {secondCatalog.books.map((book, index) => {
                            // Учитываем смещение индекса для второго каталога
                            const globalIndex = firstCatalog.books ? firstCatalog.books.length + index : index;
                            return (
                                <div
                                    key={globalIndex}
                                    className={`book ${selectedBookIndex === globalIndex ? 'selected' : ''}`}
                                >
                                    <div className="book-title">{book.title}</div>
                                    <div className="book-author">{book.author}</div>
                                    <div className="book-year">{book.year}</div>
                                    <div className="book-janre">{book.janre}</div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;