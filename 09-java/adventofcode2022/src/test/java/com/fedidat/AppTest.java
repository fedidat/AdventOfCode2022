package com.fedidat;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import org.junit.Assert;
import org.junit.Test;

public class AppTest 
{
    @Test
    public void part1Example() throws IOException
    {
        App solution = new App();
        Path path = Paths.get("src/resources/example.txt");
        List<String> content = Files.readAllLines(path);
        List<App.Move> moves = solution.parseMoves(content);
        Assert.assertEquals(13, solution.positionsVisited(moves));
    }
    @Test
    public void part1() throws IOException
    {
        App solution = new App();
        Path path = Paths.get("src/resources/input.txt");
        List<String> content = Files.readAllLines(path);
        List<App.Move> moves = solution.parseMoves(content);
        Assert.assertEquals(6044, solution.positionsVisited(moves));
    }
    @Test
    public void part2Example() throws IOException
    {
        App solution = new App(9);
        Path path = Paths.get("src/resources/example2.txt");
        List<String> content = Files.readAllLines(path);
        List<App.Move> moves = solution.parseMoves(content);
        Assert.assertEquals(36, solution.positionsVisited(moves));
    }
    @Test
    public void part2() throws IOException
    {
        App solution = new App(9);
        Path path = Paths.get("src/resources/input.txt");
        List<String> content = Files.readAllLines(path);
        List<App.Move> moves = solution.parseMoves(content);
        Assert.assertEquals(2384, solution.positionsVisited(moves));
    }
}
