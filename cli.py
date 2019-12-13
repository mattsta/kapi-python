#!/usr/bin/env python3

from pathlib import Path
import configparser
import logging
import time
import os

import click
import kapi

logger = logging.getLogger(__name__)

APP_DIR = click.get_app_dir("kapi")
APP_CONFIG = os.path.join(APP_DIR, "kapi.ini")

# ====================================================================
# Time events
# ====================================================================
class Timer:
    """ Simple way to show elapsed time for a code block """

    def __init__(self, name=""):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        self.ms = f"{self.interval * 1000:.5}"
        if self.name:
            print("Duration:", self.ms, "ms", f"[{self.name}]")
        else:
            print("Duration:", self.ms, "ms")


# ====================================================================
# Config Loader
# ====================================================================
def loadConfig(filename="api.ini"):
    config = configparser.ConfigParser()

    # Note: later files override values in earlier files. This is NOT "first file wins"
    config.read([filename, APP_CONFIG, os.path.expanduser("~/.kapi.ini")])
    if not "api" in config:
        raise Exception("Config needs [api] section!")

    key = config["api"]["key"].replace('"', "")
    kapi.key = key

    if "api_base" in config["api"]:
        # Remove quotes in case value is api_base="http://blah"
        kapi.api_base = config["api"]["api_base"].replace('"', "")


# ====================================================================
# Common container
# ====================================================================
@click.group()
def cli():
    """CLI for This is Not LinkedIn.

    Directly download and upload all your resumes, availability, connections,
    and other professional social artifacts. Use your local editors
    and source control to maintain your personal data instead of needing to rely on
    webpages for every interaction."""
    pass


# ====================================================================
# Write Config
# ====================================================================
@cli.command()
@click.option("--key", prompt="Your API Key")
def init(key):
    """ Store your API key """
    os.makedirs(APP_DIR, exist_ok=True)

    config = configparser.RawConfigParser()
    config.add_section("api")
    config.set("api", "key", key)

    with open(APP_CONFIG, "wt") as coco:
        config.write(coco)

    print("Key written to config file", APP_CONFIG)


#    print(
#        "Feel free to modify your configuration, re-run 'init', or place an override configuration file at",
#        os.path.expanduser("~/.kapi.ini"),
#    )


# ====================================================================
# Resume commands
# ====================================================================
@cli.group()
def resume():
    """ Download and upload resumes grouped by personality."""
    pass


def saveOrDump(listed, save, overwrite):
    if save:
        with Timer("Save"):
            for f in listed:
                rname = f"{f.meta.name}.json"
                dstDir = Path("docs", f.meta.personality)
                dstFile = dstDir / rname
                if os.path.isfile(dstFile) and not overwrite:
                    click.echo(
                        f"Not saving {dstFile} because it exists. Use --overwrite to clobber."
                    )
                else:
                    click.echo(f"Saving {dstFile}")
                    os.makedirs(dstDir, exist_ok=True)
                    with open(dstFile, "wt") as resume:
                        if f.resume:
                            resume.write(f.resume.jsonPretty())
                        elif f.avail:
                            resume.write(f.avail.jsonPretty())
                        else:
                            resume.write("{}\n")
    else:
        with Timer("List"):
            for f in listed:
                click.echo(f"{f.meta.personality}/{f.meta.name}")
                if f.resume:
                    click.echo(f.resume.json())
                elif f.avail:
                    click.echo(f.avail.json())
                click.echo()


@resume.command("list")
@click.option(
    "--save", is_flag=True, help="Save all resumes to docs/[personality]/[name].json"
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="When saving, overwrite existing files. Default: do not overwrite files",
)
def resumeList(save, overwrite):
    """ List your resumes and their content. Optionally save all content to files."""
    try:
        listed = kapi.Resume.list()
        saveOrDump(listed, save, overwrite)
    except:
        logger.exception("Can't list?")


@resume.command("get")
@click.argument("personality")
@click.argument("name", required=False, default=None)
def resumeGet(personality, name):
    """ Get resume for 'personality' with name 'name'.

    If 'name' is not provided, return all resumes under 'personality'. """

    try:
        got = kapi.Resume.fetch(personality=personality, resume=name)
        if isinstance(got, list):
            for g in got:
                g.debugJSON()
        else:
            got.debugJSON()
    except BaseException as e:
        logger.exception("Fetch error")

    # Usage examples
    if False:
        print(got)
        print(got.json())
        print(got.dict())
        print(got.debug())
        print(got.debugJSON())


def resumeUploadDirect(personality, name, src):
    print(f"Uploading to {personality}/{name} from {src.name}")
    with Timer("Upload"):
        try:
            sent = kapi.Resume.upload(
                personality=personality, resume=name, src=src.read()
            )
        except BaseException as e:
            logger.exception("Upload error")


@resume.command("save")
@click.argument("src", type=click.File("r"))
def resumeUploadImplicitPersonalityFromDirectoryName(src):
    """ Upload resume to personality using directory as personality name.

        If current directory is a personality name
        (see command 'resume list --save'), upload resume 'src'
        to personality name of the current directory with name of
        the current json file (with .json extension removed). """
    where = Path(src.name)
    parts = where.parts
    resumeName = parts[-1].replace(".json", "")
    personality = parts[-2]
    resumeUploadDirect(personality, name, src)


@resume.command("upload")
@click.argument("personality")
@click.argument("name")
@click.argument("src", type=click.File("r"))
def resumeUpload(personality, name, src):
    """ Upload resume 'src' to name under personality. """
    resumeUploadDirect(personality, name, src)


# ====================================================================
# Personality commands
# ====================================================================
# @cli.group()
# def personality():
#    ...


# ====================================================================
# Avail commands
# ====================================================================
@cli.group()
def avail():
    """ Download and upload availability."""
    pass


@avail.command("list")
@click.option(
    "--save", is_flag=True, help="Save all availability to src/avail/[name].json"
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="When saving, overwrite existing files. Default: do not overwrite files",
)
def availList(save, overwrite):
    """ List your availability with contents. Optionally save all content to files."""
    listed = kapi.Availability.list()
    saveOrDump(listed, save, overwrite)


def availUploadDirect(name, src):
    print(f"Uploading to avail/{name} from {src.name}")
    with Timer("Upload"):
        try:
            sent = kapi.Availability.upload(avail=name, src=src.read())
        except BaseException as e:
            logger.exception("Upload problem?")


@avail.command("save")
@click.argument("src", type=click.File("r"))
def resumeUpload(src):
    """ Upload availability 'src' to name. """
    where = Path(src.name)
    parts = where.parts
    availName = parts[-1].replace(".json", "")
    availUploadDirect(availName, src)


# ====================================================================
# Profile commands
# ====================================================================
# @cli.group()
# def profile():
#    ...


if __name__ == "__main__":
    loadConfig()
    cli()
