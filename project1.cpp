//    Library Management System
    
   

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>


#define RESET   "\033[0m"
#define CYAN    "\033[1;36m"
#define GREEN   "\033[1;32m"
#define YELLOW  "\033[1;33m"
#define RED     "\033[1;31m"
#define CLEAR() printf("\033[2J\033[H")


typedef struct {
    uint64_t id;            
    char     title[128];
    char     author[64];
    char     isbn[20];
    int      total_copies;
    int      copies_available;
} Book;

typedef struct {
    uint64_t book_id;
    char     borrower[64];
    time_t   due_date;
    int      active;         
} Loan;


#define MAX_BOOKS  1000
#define MAX_LOANS  2000

static Book  books[MAX_BOOKS];
static Loan  loans[MAX_LOANS];
static int   book_count = 0;
static int   loan_count = 0;


static uint64_t snowflake_id(void) {
    uint64_t t = (uint64_t)time(NULL);
    uint64_t r = ((uint64_t)rand() & 0xFFFF);
    return (t << 16) | r;
}

static void pause_msg(const char *msg) {
    printf(YELLOW "%s" RESET, msg);
    getchar();
}

static void load_db(void) {
    FILE *fp = fopen("library.db", "rb");
    if (!fp) return;
    fread(&book_count, sizeof(int), 1, fp);
    fread(books, sizeof(Book), book_count, fp);
    fread(&loan_count, sizeof(int), 1, fp);
    fread(loans, sizeof(Loan), loan_count, fp);
    fclose(fp);
}
static void save_db(void) {
    /* auto-backup */
    rename("library.db", "library.db.bak");
    FILE *fp = fopen("library.db", "wb");
    if (!fp) { puts(RED "Error saving database!" RESET); return; }
    fwrite(&book_count, sizeof(int), 1, fp);
    fwrite(books, sizeof(Book), book_count, fp);
    fwrite(&loan_count, sizeof(int), 1, fp);
    fwrite(loans, sizeof(Loan), loan_count, fp);
    fclose(fp);
}

void print_line(const char *c, int len) {
    for (int i = 0; i < len; i++) printf("%s", c);
    printf("\n");
}


static void add_book(void) {
    if (book_count >= MAX_BOOKS) { pause_msg("Book limit reached. Press Enter."); return; }
    Book b = { .id = snowflake_id() };
    printf("Title: ");            fgets(b.title, 128, stdin);
    printf("Author: ");           fgets(b.author, 64, stdin);
    printf("ISBN: ");             fgets(b.isbn, 20, stdin);
    printf("Total copies: ");     scanf("%d%*c",&b.total_copies);
    b.copies_available = b.total_copies;
    books[book_count++] = b;
    printf(GREEN "Added book ID %llu\n" RESET, (unsigned long long)b.id);
}

static void list_books(int verbose) {
    printf("----- Books in Catalog -----\n");
    for (int i = 0; i < book_count; ++i) {
        Book *b = &books[i];
        printf("%3d) %s by %s [%d/%d copies available]\n",
               i + 1, b->title, b->author, b->copies_available, b->total_copies);
        if (verbose) {
            printf("     ID: %llu\n", (unsigned long long)b->id);
            printf("     ISBN: %s\n", b->isbn);
        }
    }
    printf("----------------------------\n");
}

static void search_books(void) {
    char key[64]; puts("Enter keyword: "); fgets(key,64,stdin);
    int found = 0;
    for (int i = 0;i<book_count;++i) {
        Book *b=&books[i];
        if (strcasestr(b->title,key)||strcasestr(b->author,key)||strcasestr(b->isbn,key)) {
            printf("%s by %s (ID %llu)\n",b->title,b->author,(unsigned long long)b->id);
            ++found;
        }
    }
    if(!found) puts(RED "No matches." RESET);
}


static Book* find_book_by_id(uint64_t id){
    for(int i=0;i<book_count;++i) if(books[i].id==id) return &books[i];
    return NULL;
}

static void checkout_book(void){
    uint64_t id; char user[64];
    printf("Book ID: "); scanf("%llu%*c",&id);
    Book* b=find_book_by_id(id);
    if(!b){ puts(RED "Not found." RESET); return; }
    if(b->copies_available==0){ puts(RED "No copies left." RESET); return; }
    printf("Borrower name: "); fgets(user,64,stdin);
    Loan L={.book_id=id,.active=1}; strcpy(L.borrower,user);
    time_t now=time(NULL); L.due_date=now+14*24*3600; /* 2 weeks */
    loans[loan_count++]=L; b->copies_available--;
    puts(GREEN "Checked out!" RESET);
}

static void return_book(void){
    uint64_t id; printf("Book ID: "); scanf("%llu%*c",&id);
    for(int i=0;i<loan_count;++i){
        Loan* L=&loans[i];
        if(L->book_id==id && L->active){
            L->active=0;
            Book* b=find_book_by_id(id);
            if(b) b->copies_available++;
            puts(GREEN "Returned. Thank you!" RESET);
            return;
        }
    }
    puts(RED "Active loan not found." RESET);
}

static void show_overdue(void){
    puts(RED "╔══════════════════ Overdue Items ═══════════════════╗" RESET);
    time_t now=time(NULL); int count=0;
    for(int i=0;i<loan_count;++i){
        Loan*L=&loans[i]; if(!L->active) continue;
        if(difftime(L->due_date,now)<0){
            Book*b=find_book_by_id(L->book_id);
            printf("║ %-20s │ %-30.30s │ Due: %s", L->borrower, b?b->title:"(deleted)", ctime(&L->due_date));
            ++count;
        }
    }
    if(!count) puts(GREEN "║ None. 🎉                                           ║" RESET);
    puts(RED "╚════════════════════════════════════════════════════╝" RESET);
}

static void menu(void){
    int choice;
    do{
        CLEAR();
        puts(CYAN "╔════════════════════════════════════╗" RESET);
        puts(CYAN "║          LIBRARY MANAGEMENT        ║" RESET);
        puts(CYAN "║              (v2025)               ║" RESET);
        puts(CYAN "╠════════════════════════════════════╣" RESET);
        show_overdue();
        puts(CYAN "╠════════════════════════════════════╣" RESET);
        puts(CYAN "║ [1] List books                     ║" RESET);
        puts(CYAN "║ [2] Add book                       ║" RESET);
        puts(CYAN "║ [3] Search book                    ║" RESET);
        puts(CYAN "║ [4] Check-out                      ║" RESET);
        puts(CYAN "║ [5] Return                         ║" RESET);
        puts(CYAN "║ [6] Save & Exit                    ║" RESET);
        puts(CYAN "╚════════════════════════════════════╝" RESET);
        printf("Choose: ");
        scanf("%d%*c",&choice);
        switch(choice){
            case 1: list_books(1); pause_msg("Press Enter…"); break;
            case 2: add_book();    pause_msg("Press Enter…"); break;
            case 3: search_books();pause_msg("Press Enter…"); break;
            case 4: checkout_book();pause_msg("Press Enter…"); break;
            case 5: return_book(); pause_msg("Press Enter…"); break;
            case 6: break;
            default: puts("Invalid");
        }
    }while(choice!=6);
}

static void goodbye(clock_t start_tick){
    clock_t diff=clock()-start_tick;
    printf(GREEN "\nSession time: %.2fs — bye!\n" RESET,
           (double)diff/CLOCKS_PER_SEC);
}


int main(void){
    srand((unsigned)time(NULL));
    clock_t start=clock();
    load_db();
    menu();
    save_db();
    goodbye(start);
    return 0;
}