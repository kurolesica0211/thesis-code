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
Princess Nathalie of Sayn-Wittgenstein-Berleburg (Nathalie Xenia Margrethe Benedikte; born 2 May 1975) is a Danish equestrian, an Olympian, and the daughter of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She is the niece of Queen Margrethe II of Denmark and King Constantine II of Greece.
Her first cousin is King Frederik X of Denmark.
Early life

Princess Nathalie was born on 2 May 1975 in Copenhagen, Denmark, the youngest of three children of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She grew up at Schloss Berleburg in Bad Berleburg, Germany.
Nathalie and her sister Alexandra became Danish citizens on 19 May 1998.
Neither she nor her siblings are in line of succession to the Danish throne, as that would have required taking up permanent residence in Denmark when reaching the age of mandatory education.
Equestrian career

In 1994, Princess Nathalie began training at the Swedish stud Flyinge with Kyra Kyrklund, a former world champion in dressage.
Nathalie was selected as a reserve rider for the 2000 Olympic team.
She finished 12th in the individual event and helped Denmark to a 4th-place team finish.
In January 2017, Nathalie was named head coach of the Danish national dressage team.
In autumn 2005, she opened her own stud farm, which is based in Bad Berleburg.
Marriage and children

On 4 January 2010, Princess Nathalie's engagement to German horse breeder Alexander Johannsmann (born 6 December 1977), son of showjumper Heinrich-Wilhelm Johannsmann, was announced.
The couple married civilly 27 May 2010 and religiously the following year, on 18 June 2011 at the Protestant Stadtkirche in Berleburg, Germany.
Princess Nathalie gave birth to a son, Konstantin Gustav Heinrich Richard, on 24 July 2010.
Konstantin's godparents were Crown Princess Mary of Denmark, his aunt Ann-Kathrin Johannsmann, and his uncle Prince Gustav.
On 28 January 2015, she gave birth to her second child, a daughter named Louisa Margareta Benedikte Hanna, in Bad Berleburg, Germany.
On 15 August 2022, the Danish court confirmed that Nathalie and Johannsmann had divorced.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (c77e16fa-d0ac-47b2-987d-8119b177a20a)
 Call ID: c77e16fa-d0ac-47b2-987d-8119b177a20a
  Args:
    type: :Woman
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (319c3cc0-93a9-4cda-a32a-5439e64be234)
 Call ID: 319c3cc0-93a9-4cda-a32a-5439e64be234
  Args:
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddLiteral (a9e5b46d-ab1f-43ce-a68d-037ac205a2af)
 Call ID: a9e5b46d-ab1f-43ce-a68d-037ac205a2af
  Args:
    literal_value: 1975
    relation: :hasBirthYear
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
  AssignClass (38d800dd-c848-483d-8a60-e037d9b7b40f)
 Call ID: 38d800dd-c848-483d-8a60-e037d9b7b40f
  Args:
    source: :Benedikte_of_Denmark
    type: :Woman
  AssignClass (51de73ba-b7d3-4620-bc97-1da91f121ac6)
 Call ID: 51de73ba-b7d3-4620-bc97-1da91f121ac6
  Args:
    type: :Person
    source: :Benedikte_of_Denmark
  AssignClass (1589c50a-dc64-4e12-9285-393e0377634d)
 Call ID: 1589c50a-dc64-4e12-9285-393e0377634d
  Args:
    source: :Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (1b6aae35-6fc1-4959-9d84-357f9c283dbd)
 Call ID: 1b6aae35-6fc1-4959-9d84-357f9c283dbd
  Args:
    source: :Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AddTriple (7937ded6-69b4-4516-894a-691920ee4458)
 Call ID: 7937ded6-69b4-4516-894a-691920ee4458
  Args:
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMother
    target: :Benedikte_of_Denmark
  AddTriple (c92b6148-7f48-4c5b-9f19-97d5c2f7ce85)
 Call ID: c92b6148-7f48-4c5b-9f19-97d5c2f7ce85
  Args:
    target: :Richard_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (50ea2c6c-5860-4b12-b794-add6e32b8af9)
 Call ID: 50ea2c6c-5860-4b12-b794-add6e32b8af9
  Args:
    type: :Woman
    source: :Margrethe_II_of_Denmark
  AssignClass (475cb856-b9ef-45ef-ba65-bcdd14d4547b)
 Call ID: 475cb856-b9ef-45ef-ba65-bcdd14d4547b
  Args:
    type: :Person
    source: :Margrethe_II_of_Denmark
  AssignClass (ea10f251-f21b-4d99-90c5-649e840e6df0)
 Call ID: ea10f251-f21b-4d99-90c5-649e840e6df0
  Args:
    source: :Constantine_II_of_Greece
    type: :Man
  AssignClass (12151970-c27d-42c3-baed-d7b41fe49ce4)
 Call ID: 12151970-c27d-42c3-baed-d7b41fe49ce4
  Args:
    type: :Person
    source: :Constantine_II_of_Greece
  AssignClass (0a7539cc-376d-45b8-84d9-5f489d80d84c)
 Call ID: 0a7539cc-376d-45b8-84d9-5f489d80d84c
  Args:
    type: :Man
    source: :Frederik_X_of_Denmark
  AssignClass (b5cd4d76-52c1-4f7b-9d39-9ea2e216aeb8)
 Call ID: b5cd4d76-52c1-4f7b-9d39-9ea2e216aeb8
  Args:
    type: :Person
    source: :Frederik_X_of_Denmark
  AssignClass (3a44b590-cdb9-43d7-84af-87085224a948)
 Call ID: 3a44b590-cdb9-43d7-84af-87085224a948
  Args:
    source: :Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (728df5a4-9ec2-4f4d-afa3-8a2b7f6f8600)
 Call ID: 728df5a4-9ec2-4f4d-afa3-8a2b7f6f8600
  Args:
    type: :Person
    source: :Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (7b62b30b-352f-454d-a201-9910221140ec)
 Call ID: 7b62b30b-352f-454d-a201-9910221140ec
  Args:
    target: :Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasSister
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (57a5d5d1-3750-4e70-af26-e4360d083c87)
 Call ID: 57a5d5d1-3750-4e70-af26-e4360d083c87
  Args:
    source: :Alexander_Johannsmann
    type: :Man
  AssignClass (62886273-de80-45c2-8c53-738bf6e252d9)
 Call ID: 62886273-de80-45c2-8c53-738bf6e252d9
  Args:
    source: :Alexander_Johannsmann
    type: :Person
  AddLiteral (d8b017be-46b2-4bf6-a9f9-44d7bfd9e327)
 Call ID: d8b017be-46b2-4bf6-a9f9-44d7bfd9e327
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    source: :Alexander_Johannsmann
    literal_type: xsd:integer
  AssignClass (6712e88d-8969-4e21-8699-b1ee23812b6f)
 Call ID: 6712e88d-8969-4e21-8699-b1ee23812b6f
  Args:
    source: :Heinrich-Wilhelm_Johannsmann
    type: :Man
  AssignClass (733170ac-0f17-41c6-aaf2-d8f593278c68)
 Call ID: 733170ac-0f17-41c6-aaf2-d8f593278c68
  Args:
    type: :Person
    source: :Heinrich-Wilhelm_Johannsmann
  AddTriple (dc0c56bb-a790-414a-9f0e-d122991f79ba)
 Call ID: dc0c56bb-a790-414a-9f0e-d122991f79ba
  Args:
    relation: :hasFather
    source: :Alexander_Johannsmann
    target: :Heinrich-Wilhelm_Johannsmann
  AddLiteral (4add3eac-21bd-4407-954f-2e176dddf080)
 Call ID: 4add3eac-21bd-4407-954f-2e176dddf080
  Args:
    literal_value: 2010
    source: :Nathalie_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (11f45589-24bc-4dcf-86db-b61d70fe37d1)
 Call ID: 11f45589-24bc-4dcf-86db-b61d70fe37d1
  Args:
    source: :Konstantin_Gustav_Heinrich_Richard
    type: :Man
  AssignClass (002af10f-9d13-4bd3-b982-1c37a015b147)
 Call ID: 002af10f-9d13-4bd3-b982-1c37a015b147
  Args:
    source: :Konstantin_Gustav_Heinrich_Richard
    type: :Person
  AddLiteral (dbc3bdb0-9054-4cff-91a3-af9036cc9c17)
 Call ID: dbc3bdb0-9054-4cff-91a3-af9036cc9c17
  Args:
    literal_value: 2010
    relation: :hasBirthYear
    source: :Konstantin_Gustav_Heinrich_Richard
    literal_type: xsd:integer
  AddTriple (112ffbde-813f-459b-8627-33dcf1d55457)
 Call ID: 112ffbde-813f-459b-8627-33dcf1d55457
  Args:
    source: :Konstantin_Gustav_Heinrich_Richard
    relation: :hasMother
    target: :Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (0dcb2fff-c6c0-42ed-9ede-62375493af33)
 Call ID: 0dcb2fff-c6c0-42ed-9ede-62375493af33
  Args:
    target: :Alexander_Johannsmann
    relation: :hasFather
    source: :Konstantin_Gustav_Heinrich_Richard
  AssignClass (ef358aea-062d-4b65-a4d0-58c28a318b96)
 Call ID: ef358aea-062d-4b65-a4d0-58c28a318b96
  Args:
    type: :Woman
    source: :Ann-Kathrin_Johannsmann
  AssignClass (29357452-d748-434b-a2ae-a3c62d34c2a0)
 Call ID: 29357452-d748-434b-a2ae-a3c62d34c2a0
  Args:
    source: :Ann-Kathrin_Johannsmann
    type: :Person
  AssignClass (70c57220-f017-4cbb-9ef8-d7ae3ee7a848)
 Call ID: 70c57220-f017-4cbb-9ef8-d7ae3ee7a848
  Args:
    source: :Gustav_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (6d5dd7da-bc09-4f3b-97e7-0d806be9fe98)
 Call ID: 6d5dd7da-bc09-4f3b-97e7-0d806be9fe98
  Args:
    source: :Gustav_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (dd691528-17ff-4912-ae72-298e8a5de898)
 Call ID: dd691528-17ff-4912-ae72-298e8a5de898
  Args:
    type: :Woman
    source: :Louisa_Margareta_Benedikte_Hanna
  AssignClass (46940377-f8d6-445d-96dc-8b5fb7d0fe28)
 Call ID: 46940377-f8d6-445d-96dc-8b5fb7d0fe28
  Args:
    source: :Louisa_Margareta_Benedikte_Hanna
    type: :Person
  AddLiteral (a359ee5a-f6a3-43d7-b3c1-ee96698cd70e)
 Call ID: a359ee5a-f6a3-43d7-b3c1-ee96698cd70e
  Args:
    source: :Louisa_Margareta_Benedikte_Hanna
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2015
  AddTriple (6657a702-0067-43f6-b2e8-e8255517c7ef)
 Call ID: 6657a702-0067-43f6-b2e8-e8255517c7ef
  Args:
    target: :Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: :Louisa_Margareta_Benedikte_Hanna
    relation: :hasMother
  AddTriple (751ac6ff-bf97-415c-9e57-d8c01ff666f1)
 Call ID: 751ac6ff-bf97-415c-9e57-d8c01ff666f1
  Args:
    target: :Alexander_Johannsmann
    relation: :hasFather
    source: :Louisa_Margareta_Benedikte_Hanna
  Finish (f397de31-165e-4d8d-9844-506f0a8d3972)
 Call ID: f397de31-165e-4d8d-9844-506f0a8d3972
  Args: