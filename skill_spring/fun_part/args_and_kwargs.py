class ArgsKwargsDemo:
    """Utility to demonstrate handling of *args and **kwargs."""

    @staticmethod
    def format_args(*args) -> str:
        if not args:
            return "Positional arguments (*args): (none)"
        lines = ["Positional arguments (*args):"]
        lines += [f"  args[{i}] = {value}" for i, value in enumerate(args)]
        return "\n".join(lines)

    @staticmethod
    def format_kwargs(**kwargs) -> str:
        if not kwargs:
            return "Named arguments (**kwargs): (none)"
        lines = ["Named arguments (**kwargs):"]
        lines += [f"  {key} = {value}" for key, value in kwargs.items()]
        return "\n".join(lines)

    def show(self, *args, **kwargs) -> None:
        """Print formatted args and kwargs."""
        print(self.format_args(*args))
        print()
        print(self.format_kwargs(**kwargs))


if __name__ == "__main__":
    demo = ArgsKwargsDemo()
    demo.show(1, 2, a=3, b=4, c=5)
