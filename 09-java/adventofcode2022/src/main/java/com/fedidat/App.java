package com.fedidat;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class App {

    public record Move(char direction, int offset) {
    }

    public List<Move> parseMoves(List<String> content) {
        List<Move> moves = content.stream()
                .map(line -> new Move(line.charAt(0), Integer.parseInt(line.substring(2))))
                .collect(Collectors.toList());
        return moves;
    }

    private Position head = new Position(0, 0);
    private Map<Integer, Position> chains = new HashMap<>();
    private Set<Position> visited = new HashSet<>() {{
        add(new Position(0, 0));
    }};

    public App() {
        this(1);
    }

    public App(int ropeSize) {
        for (int i = 1; i <= ropeSize; i++) {
            this.chains.put(i, new Position(0, 0));
        }
    }

    public record Position(int x, int y) {
        public Position offset(Position offset) {
            return new Position(this.x + offset.x, this.y + offset.y);
        }
    }

    private static final Map<Character, Position> MOVE_OFFSETS = Map.of(
            'R', new Position(1, 0),
            'L', new Position(-1, 0),
            'U', new Position(0, 1),
            'D', new Position(0, -1));

    private void makeMove(Move move) {
        for (int i = 0; i < move.offset(); i++) {
            for (int chain = 0; chain < chains.size(); chain++) {
                Position old = chains.get(chain);
                if (chain == 0) // for chain 0, take previous position as head and move it
                    head = old = head.offset(MOVE_OFFSETS.get(move.direction()));
                chains.put(chain + 1, follow(chains.get(chain + 1), old));
            }
            visited.add(chains.get(chains.size()));
        }
    }

    private Position follow(Position follower, Position followee) {
        if (Math.abs(follower.y - followee.y) <= 1 && Math.abs(follower.x - followee.x) <= 1)
            return follower; // we won't move, return
        return follower.offset(new Position(Integer.signum(followee.x - follower.x),
                Integer.signum(followee.y - follower.y)));
    }

    public int positionsVisited(List<Move> moves) {
        for (Move move : moves)
            this.makeMove(move);
        return visited.size();
    }
}
