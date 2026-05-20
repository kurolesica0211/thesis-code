================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Baroness Armgard of Sierstorpff-Cramm, known as Armgard von Cramm (German: Armgard Kunigunde Alharda Agnes Oda von Cramm; 18 December 1883 – 27 April 1971) was the mother of Prince Bernhard of Lippe-Biesterfeld, Prince consort of Queen Juliana of the Netherlands.
Early life

Armgard was born at Bad Driburg, Kingdom of Prussia (now in North Rhine-Westphalia, Germany), as the fourth child and fourth daughter of Baron Aschwin of Sierstorpff-Cramm, and his wife, Baroness Hedwig of Sierstorpff-Driburg.
By birth, she belonged to the ancient German Cramm family.
Marriages

Armgard married on 24 October 1905 at Hanover to Count Bodo von Oeynhausen, an officer in the 8th Hussars in Paderborn, son of Count Erich von Oeynhausen and his wife, Therese von Lenthe.
Armgard married secondly, after the death of her ex-husband, on 4 March 1909 at Oelber, Brunswick to Prince Bernhard of Lippe-Biesterfeld, a younger son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of the Principality of Lippe, and his wife, Countess Karoline von Wartensleben.
The marriage was at first considered morganatic, as Armgard's family didn't belong to one of the reigning or former reigning families.
Thus, she was created "Countess of Biesterfeld" (German: Gräfin von Biesterfeld) on 8 February 1909.
On 24 February 1916, her marriage was declared equal and she was made "Princess of Lippe-Biesterfeld" (German: Prinzessin zur Lippe-Biesterfeld) along with the style Serene Highness by her brother-in-law, Leopold IV, Prince of Lippe, and this title was extended to her two sons in order to produce a new branch of the Lippe family.
World War II

After the death of her husband in 1934, Armgard moved into Reckenwalde palace with her sons and managed an estate in Wojnowo, Lubusz Voivodeship, Province of Brandenburg (now Wojnowo, Poland), together with her new partner, Alexis Pantchoulidzew, an exiled Russian nobleman.
Alexis accompanied Armgard to the wedding of Bernhard to Princess Juliana.
During World War II Armgard and Alexis were observed by the local Gestapo.
The SS demanded in September 1944 in Recke, one of Armgard's properties, Schloss Woynowo Walde for military purposes.
Armgard and Alexis gave an account of the withdrawal in 1945 of the Wehrmacht behind the Oder-line on their estate at Neumark.
Wim Klinkenberg and some other writers have accused Armgard of sexual promiscuity, intrigue, conspiracy, and – as with her son Aschwin – of Nazi sympathies.
In March 2004, her son Bernhard tried to rectify this image with an open letter to The Times.
Armgard was a convert to Roman Catholicism like her granddaughter Princess Irene, but decided against attending Irene's controversial wedding to Carlos Hugo, Duke of Parma, which neither the Dutch royal family nor any Dutch diplomatic representative attended.
The family nevertheless gathered at Armgard's home for the television coverage of the wedding.
Death

Armgard died on 27 April 1971 in House Warmelo in Diepenheim, at the age of 87.
Zur Lippe-Biesterfeld- Prof. mr. E.J.H.Schrage



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (18cf9d48-8cd4-42b9-bd1b-22a0b9380c8f)
 Call ID: 18cf9d48-8cd4-42b9-bd1b-22a0b9380c8f
  Args:
    type: :Woman
    source: Armgard_von_Cramm
  AssignClass (1a6ff408-0ef5-4300-a6cc-9b087f97edad)
 Call ID: 1a6ff408-0ef5-4300-a6cc-9b087f97edad
  Args:
    type: :Person
    source: Armgard_von_Cramm
  AddLiteral (6cfb520c-4617-4b79-9511-129a715e8dd1)
 Call ID: 6cfb520c-4617-4b79-9511-129a715e8dd1
  Args:
    source: Armgard_von_Cramm
    literal_type: xsd:string
    literal_value: Armgard von Cramm
    relation: :knownAs
  AddLiteral (496b2679-3cc8-44f3-ab26-af67e246992b)
 Call ID: 496b2679-3cc8-44f3-ab26-af67e246992b
  Args:
    source: Armgard_von_Cramm
    literal_type: xsd:integer
    literal_value: 1883
    relation: :hasBirthYear
  AddLiteral (35b62b1c-d494-4f85-9342-b55ea68eb68f)
 Call ID: 35b62b1c-d494-4f85-9342-b55ea68eb68f
  Args:
    relation: :hasDeathYear
    literal_value: 1971
    literal_type: xsd:integer
    source: Armgard_von_Cramm
  AssignClass (7f41fb83-80d7-43a2-9cf7-c5e8591fe9de)
 Call ID: 7f41fb83-80d7-43a2-9cf7-c5e8591fe9de
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (2829c0f6-4b9b-4e16-a02c-b1aee5caa568)
 Call ID: 2829c0f6-4b9b-4e16-a02c-b1aee5caa568
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (757f4428-f445-4270-be15-4939d3eadf21)
 Call ID: 757f4428-f445-4270-be15-4939d3eadf21
  Args:
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe-Biesterfeld
    target: Armgard_von_Cramm
  AssignClass (d41be46b-3f46-463c-a232-0f53e62bc3fc)
 Call ID: d41be46b-3f46-463c-a232-0f53e62bc3fc
  Args:
    type: :Man
    source: Baron_Aschwin_of_Sierstorpff-Cramm
  AssignClass (a0f6f01a-e930-4aae-8007-35410ab7a51e)
 Call ID: a0f6f01a-e930-4aae-8007-35410ab7a51e
  Args:
    type: :Person
    source: Baron_Aschwin_of_Sierstorpff-Cramm
  AssignClass (266bb4e4-fdab-41c9-81cf-1765c6ab3615)
 Call ID: 266bb4e4-fdab-41c9-81cf-1765c6ab3615
  Args:
    type: :Ancestor
    source: Baron_Aschwin_of_Sierstorpff-Cramm
  AssignClass (9623b5c5-02b5-4f27-a662-d302765781fb)
 Call ID: 9623b5c5-02b5-4f27-a662-d302765781fb
  Args:
    type: :Woman
    source: Baroness_Hedwig_of_Sierstorpff-Driburg
  AssignClass (6c0dfc33-2ac6-4a31-8c66-7bdef55c62b0)
 Call ID: 6c0dfc33-2ac6-4a31-8c66-7bdef55c62b0
  Args:
    type: :Person
    source: Baroness_Hedwig_of_Sierstorpff-Driburg
  AssignClass (4bf3692d-8b8f-4e20-bfd1-1a1429ffc950)
 Call ID: 4bf3692d-8b8f-4e20-bfd1-1a1429ffc950
  Args:
    type: :Ancestor
    source: Baroness_Hedwig_of_Sierstorpff-Driburg
  AddTriple (2f7a0ed6-97f1-4155-ac24-73c697ef448b)
 Call ID: 2f7a0ed6-97f1-4155-ac24-73c697ef448b
  Args:
    relation: :hasFather
    source: Armgard_von_Cramm
    target: Baron_Aschwin_of_Sierstorpff-Cramm
  AddTriple (d06adfcc-7a84-44d2-922c-d96364243f5e)
 Call ID: d06adfcc-7a84-44d2-922c-d96364243f5e
  Args:
    target: Baroness_Hedwig_of_Sierstorpff-Driburg
    source: Armgard_von_Cramm
    relation: :hasMother
  AssignClass (c25d14c1-c771-4233-ac2c-d4af9b1c21dc)
 Call ID: c25d14c1-c771-4233-ac2c-d4af9b1c21dc
  Args:
    type: :Man
    source: Count_Bodo_von_Oeynhausen
  AssignClass (73ff6614-0ac8-4847-9274-dcd31cffd077)
 Call ID: 73ff6614-0ac8-4847-9274-dcd31cffd077
  Args:
    type: :Person
    source: Count_Bodo_von_Oeynhausen
  AddLiteral (db5b310b-c71b-4632-a327-b9af1df30c47)
 Call ID: db5b310b-c71b-4632-a327-b9af1df30c47
  Args:
    literal_type: xsd:integer
    literal_value: 1905
    source: Armgard_von_Cramm
    relation: :hasMarriageYear
  AddTriple (733a25a4-5cb7-408e-86cd-764ca9d59767)
 Call ID: 733a25a4-5cb7-408e-86cd-764ca9d59767
  Args:
    relation: :hasRelation
    source: Armgard_von_Cramm
    target: Count_Bodo_von_Oeynhausen
  AssignClass (ee0c52b4-5254-4563-b4e3-5b03acd53404)
 Call ID: ee0c52b4-5254-4563-b4e3-5b03acd53404
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AssignClass (d633d618-0a89-40d7-ba5a-218860d0c9fc)
 Call ID: d633d618-0a89-40d7-ba5a-218860d0c9fc
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AssignClass (068f9a14-e6ab-426b-9e32-4c310b6464b6)
 Call ID: 068f9a14-e6ab-426b-9e32-4c310b6464b6
  Args:
    type: :Ancestor
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
  AddLiteral (736e66e4-8fb4-4c2c-8aed-dd411d4be1ae)
 Call ID: 736e66e4-8fb4-4c2c-8aed-dd411d4be1ae
  Args:
    relation: :hasMarriageYear
    literal_value: 1909
    literal_type: xsd:integer
    source: Armgard_von_Cramm
  AddTriple (348ea765-7280-4fc4-bc73-35e4199002d8)
 Call ID: 348ea765-7280-4fc4-bc73-35e4199002d8
  Args:
    target: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
    source: Armgard_von_Cramm
    relation: :hasRelation
  AssignClass (ad5caf7a-1794-4e7e-b2c9-7e8ef9452590)
 Call ID: ad5caf7a-1794-4e7e-b2c9-7e8ef9452590
  Args:
    type: :Man
    source: Count_Erich_von_Oeynhausen
  AssignClass (cbed5fdc-c561-425d-a668-12a3c1d3b237)
 Call ID: cbed5fdc-c561-425d-a668-12a3c1d3b237
  Args:
    type: :Person
    source: Count_Erich_von_Oeynhausen
  AssignClass (e2d8ce82-0434-477c-9c47-3cf43254986b)
 Call ID: e2d8ce82-0434-477c-9c47-3cf43254986b
  Args:
    type: :Ancestor
    source: Count_Erich_von_Oeynhausen
  AssignClass (cc7a9524-e800-45a8-b84b-8f9c6e0cb6be)
 Call ID: cc7a9524-e800-45a8-b84b-8f9c6e0cb6be
  Args:
    type: :Woman
    source: Therese_von_Lenthe
  AssignClass (d9bc1d6e-16a8-4d68-b93c-7701f35eb307)
 Call ID: d9bc1d6e-16a8-4d68-b93c-7701f35eb307
  Args:
    type: :Person
    source: Therese_von_Lenthe
  AssignClass (afeb5fad-3609-48f2-a03a-cdc71ceb0681)
 Call ID: afeb5fad-3609-48f2-a03a-cdc71ceb0681
  Args:
    type: :Ancestor
    source: Therese_von_Lenthe
  AddTriple (73c49696-0e7c-405d-bcfe-5f8534f046da)
 Call ID: 73c49696-0e7c-405d-bcfe-5f8534f046da
  Args:
    relation: :hasFather
    source: Count_Bodo_von_Oeynhausen
    target: Count_Erich_von_Oeynhausen
  AddTriple (7c2d9739-05b1-40b8-aaae-8a196de4bef1)
 Call ID: 7c2d9739-05b1-40b8-aaae-8a196de4bef1
  Args:
    target: Therese_von_Lenthe
    source: Count_Bodo_von_Oeynhausen
    relation: :hasMother
  AssignClass (b9d193e1-9373-4c6c-b57e-161858173b40)
 Call ID: b9d193e1-9373-4c6c-b57e-161858173b40
  Args:
    type: :Man
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (48968e4e-2a15-4af2-be23-c7eacad07b13)
 Call ID: 48968e4e-2a15-4af2-be23-c7eacad07b13
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (73952c91-09d6-4679-aa05-41a78579ee27)
 Call ID: 73952c91-09d6-4679-aa05-41a78579ee27
  Args:
    type: :Ancestor
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (41415acf-211e-472b-94f4-91e54733b221)
 Call ID: 41415acf-211e-472b-94f4-91e54733b221
  Args:
    type: :Woman
    source: Countess_Karoline_von_Wartensleben
  AssignClass (2e6af18b-edb2-4ac1-9539-c6bc3d0d45a5)
 Call ID: 2e6af18b-edb2-4ac1-9539-c6bc3d0d45a5
  Args:
    type: :Person
    source: Countess_Karoline_von_Wartensleben
  AssignClass (d884f1a4-f1b6-41c0-89dc-af7daed948d3)
 Call ID: d884f1a4-f1b6-41c0-89dc-af7daed948d3
  Args:
    type: :Ancestor
    source: Countess_Karoline_von_Wartensleben
  AddTriple (d4bf91e1-27b2-4738-9e9f-bd66199bb89a)
 Call ID: d4bf91e1-27b2-4738-9e9f-bd66199bb89a
  Args:
    target: Ernest_II_Count_of_Lippe-Biesterfeld
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
    relation: :hasFather
  AddTriple (a892b46a-7ab7-497c-a43a-7ecfc3f0cdb5)
 Call ID: a892b46a-7ab7-497c-a43a-7ecfc3f0cdb5
  Args:
    relation: :hasMother
    source: Prince_Bernhard_of_Lippe-Biesterfeld_Senior
    target: Countess_Karoline_von_Wartensleben
  AssignClass (8ffa4035-faa4-4bc4-bbab-501df53862fd)
 Call ID: 8ffa4035-faa4-4bc4-bbab-501df53862fd
  Args:
    type: :Man
    source: Aschwin_of_Lippe-Biesterfeld
  AssignClass (1563e852-0900-42f5-99a5-a90870bfa2f4)
 Call ID: 1563e852-0900-42f5-99a5-a90870bfa2f4
  Args:
    type: :Person
    source: Aschwin_of_Lippe-Biesterfeld
  AddTriple (7faf7fb3-9a8a-4317-9499-6c4f6087f72d)
 Call ID: 7faf7fb3-9a8a-4317-9499-6c4f6087f72d
  Args:
    target: Armgard_von_Cramm
    source: Aschwin_of_Lippe-Biesterfeld
    relation: :hasMother
  AssignClass (e3a42274-63c3-4f8b-9e87-077c8c4ecf05)
 Call ID: e3a42274-63c3-4f8b-9e87-077c8c4ecf05
  Args:
    type: :Man
    source: Alexis_Pantchoulidzew
  AssignClass (e01b520d-c092-4ee7-8091-b5f62876cd4b)
 Call ID: e01b520d-c092-4ee7-8091-b5f62876cd4b
  Args:
    type: :Person
    source: Alexis_Pantchoulidzew
  AssignClass (184a2a44-7d04-4818-b9c5-65fffc78054d)
 Call ID: 184a2a44-7d04-4818-b9c5-65fffc78054d
  Args:
    type: :Woman
    source: Princess_Irene
  AssignClass (4686c13b-f279-40db-9008-81f7ac464474)
 Call ID: 4686c13b-f279-40db-9008-81f7ac464474
  Args:
    type: :Person
    source: Princess_Irene
  Finish (50c659c0-3b5a-41b9-96b3-379614cf7563)
 Call ID: 50c659c0-3b5a-41b9-96b3-379614cf7563
  Args: