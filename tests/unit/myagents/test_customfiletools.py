import unittest
from pathlib import Path

from agentxs.myagents import customfiletools
from agentxs.myagents.agentwrapper import AgentWrapperContext



class TestCustomTools(unittest.TestCase):

    def test_get_available_files(self):

        context = AgentWrapperContext(available_path=str(Path(__file__).parent.joinpath("packagefortesting")),
                                      available_extensions=(".py", ".txt"))
        available_files = customfiletools._get_available_files_impl(context=context)

        self.assertEqual(8, len(available_files))
        for file in available_files:
            abs_file = Path(context.available_path).joinpath(file)
            self.assertTrue(abs_file.is_file())
            self.assertTrue(str(abs_file).endswith(context.available_extensions))

        context.available_extensions = (".py",)
        available_files = customfiletools._get_available_files_impl(context=context)
        self.assertEqual(7, len(available_files))
        for file in available_files:
            abs_file = Path(context.available_path).joinpath(file)
            self.assertTrue(abs_file.is_file())
            self.assertTrue(str(abs_file).endswith(context.available_extensions))

    def test_get_paths_from_filename(self):
        context = AgentWrapperContext(available_path=str(Path(__file__).parent.joinpath("packagefortesting")),
                                      available_extensions=(".py",))
        context.available_extensions = (".py",)

        results = customfiletools._get_paths_from_filename_impl(context=context, filename="asubpackage")
        self.assertEqual(0, len(results))

        results = customfiletools._get_paths_from_filename_impl(context=context, filename="fileatsubpackage.py")
        self.assertEqual(1, len(results))
        self.assertTrue(Path(results[0]).is_file())

        results = customfiletools._get_paths_from_filename_impl(context=context, filename="file.txt")
        self.assertEqual(0, len(results))

        # Testing a pattern.
        results = customfiletools._get_paths_from_filename_impl(context=context, filename="file*.*")
        self.assertEqual(3, len(results))

    def test_get_file_content(self):
        content = customfiletools._get_file_content_impl(str(Path(__file__).parent.joinpath("packagefortesting").joinpath("fileatroot.py")))
        self.assertTrue(isinstance(content, str))

