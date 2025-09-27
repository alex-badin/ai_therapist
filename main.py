from core.orchestrator import TherapyOrchestrator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

def main():
    console.print("\n[bold cyan]🧠 Мультиагентная Терапевтическая Система[/bold cyan]")
    console.print("[yellow]" + "="*60 + "[/yellow]")
    console.print("[red]⚠️  Это образовательная демонстрация, не для реального использования[/red]")
    console.print("[dim]Команды: 'выход' - завершить, 'память' - показать инсайты[/dim]\n")
    
    orchestrator = TherapyOrchestrator(use_memory=True)
    session_id = orchestrator.start_session()
    
    console.print(f"[green]✓ Сессия начата (ID: {session_id})[/green]\n")
    
    while True:
        user_input = console.input("[bold blue]Вы:[/bold blue] ").strip()
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            console.print("\n[yellow]👋 Сессия завершена. Берегите себя![/yellow]")
            break
        
        if user_input.lower() in ['память', 'memory']:
            insights = orchestrator.get_session_insights()
            if insights:
                table = Table(title="📚 Инсайты Сессии")
                table.add_column("Тип", style="cyan")
                table.add_column("Инсайт", style="white")
                table.add_column("Подход", style="green")
                
                for ins in insights[:5]:
                    table.add_row(
                        ins['type'].upper(),
                        ins['insight'],
                        ins['approach']
                    )
                
                console.print(table)
            else:
                console.print("[dim]Пока нет инсайтов[/dim]")
            continue
        
        # Обработка сообщения
        with console.status("[yellow]Обработка...[/yellow]"):
            result = orchestrator.process_message(user_input)
        
        # Показываем метаинформацию
        approach_colors = {
            "DBT": "blue",
            "IFS": "magenta",
            "TRE": "green"
        }
        color = approach_colors.get(result['approach'], 'white')
        
        panel = Panel(
            result['response'],
            title=f"[{color}]{result['approach']}[/{color}] Специалист",
            subtitle=f"[dim]{result['reasoning']} (уверенность: {result['confidence']:.0%})[/dim]"
        )
        console.print(panel)
        
        # Показываем инсайты если есть
        if result.get('insights') and result['insights'].get('insights'):
            rprint(f"[dim]💡 Инсайты: {', '.join(result['insights']['insights'])}[/dim]")

if __name__ == "__main__":
    main()