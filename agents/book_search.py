import pandas as pd 
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import logging
from pandas.core.internals import SingleBlockManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

mcp = FastMCP("book_search")

books_df = Path(__file__).parent / "GoodReads_100k_books.csv"

@mcp.tool()
def search(genre: str, pages_number: int) -> pd.DataFrame:
    """
    descricao: 
    Função para buscar livros dentro de uma df de dados
    a partir de um genre e numero de páginas. 
    Importante que genre seja passado em inglês. 

    Args:
        genre (string): nome do genre (inglês)
        pages_number (int): numero de paginas do livro

    Returns:
        dataframe: livros encontrados com as colunas: 
         'author', 'bookformat', 'desc', 'genre', 'img', 'isbn', 'isbn13',
       'link', 'pages', 'rating', 'reviews', 'title', 'totalratings'
    """   
    print("essa que deu erro?")

    df = pd.read_csv(books_df, encoding= 'utf-8')
    df['pages'] = df['pages'].astype(int)
    df['rating'] = df['rating'].astype(float)
    df = df[(df['genre'].str.contains(genre, case=False)) & ((pages_number-20)<df['pages']) & (df['pages']<(pages_number+20))]

    if len(df)>100:
        df_4 = df[df['rating']>4]
        if len(df_4) >0:
            df = df_4

    df = df.sort_values(by="rating", ascending=False)
    result = df[['title', 'author', 'pages', 'genre', 'rating', 'desc']].head(10).to_dict(orient='records')

    return result

@mcp.tool()
def search_by_name(title: str):
    """
    descricao: 
    Função para buscar as informações de um 
    livro dentro de uma df de dados
    a partir do nome dele. 
    Importante que o nome do livro seja passado em inglês. 

    Args:
        title (string): nome do livro (inglês)

    Returns:
        dict: informações do livro: 
        author: The name of the author/authors of the book
        bookformat: The format of the book
        desc: The description of the book
        genre: The list of genres related to the book
        img: Image link of the book
        isbn: ISBN code of the book
        isbn13: ISBN13 code of the book
        link: The goodreads links of the book
        pages: Number of pages in the book
        rating: Average rating of the book
        reviews: The number of reviews the book has
        title: The title of the book
        totalratings: Totalratings of the book
    """   
    df = pd.read_csv(books_df, encoding= 'utf-8')

    df = df[df['title'].str.contains(title, case=False, na=False)]

    return df


if __name__ == "__main__":
    mcp.run(transport="stdio", timeout=30)