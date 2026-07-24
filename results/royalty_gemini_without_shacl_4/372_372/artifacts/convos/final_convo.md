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
Prince George William of Hanover and Cumberland (Georg Wilhelm Ernst August Friedrich Axel Prinz von Hannover; 25 March 1915 – 8 January 2006) was the second-eldest son of Ernest Augustus, Duke of Brunswick, and his wife Princess Victoria Louise of Prussia, the only daughter of Wilhelm II, German Emperor, and Augusta Victoria of Schleswig-Holstein.
George William's wife was a sister of Prince Philip, Duke of Edinburgh, and his children are thus first cousins of King Charles III.
His sister, Frederica, became Queen of the Hellenes as the consort of King Paul of Greece.
He held the title of Prince of the United Kingdom of Great Britain and Ireland, granted ad personam to the children of the then-Duke of Brunswick by George V's letters patent of 1914, which remained unrevoked.
Life

George William was christened on 10 May 1915 in Brunswick.
The prince's godparents included Maria Christina of Austria, Prince Axel of Denmark, and Princess Olga of Hanover and Cumberland who held the infant prince over the baptismal font.
From 1930 through 1934, Prince George William attended the elite boarding school Schule Schloss Salem in Überlingen on Lake Constance.
Schule Schloss Salem was co-founded by the prince's uncle, the last Chancellor of the German Empire, Prince Maximilian of Baden, and educator Kurt Hahn in 1920.
A former student of the institution, the prince then went to Scotland with his wife to meet with Kurt Hahn, the founder of the school, and to visit Gordonstoun, the establishment that the latter founded when he had to flee Nazi Germany because of his Jewish origins.
Together with his wife, as well as his three brothers, he took part in the ship tours organized by his sister Queen Frederica and her husband King Paul of Greece in 1954 and 1956, which became known as the “Cruises of the Kings” and were attended by over 100 royals from all over Europe.
For many years Prince George William was a member of the International Olympic Committee (IOC) and of the Deutscher Olympischer Sportbund (DOSB), the German NOC.
Prince George William of Hanover lived in Schliersee, near Munich, and died in Munich in 2006 aged 90.
His wife, Sophie, sister of Prince Philip of Greece and Denmark, later Duke of Edinburgh, consort of Queen Elizabeth II of the United Kingdom, died in 2001.
Marriage

On 23 April 1946 in Salem, Baden-Württemberg, Germany, Prince George William married his third cousin Princess Sophie of Greece and Denmark, daughter of Prince Andrew of Greece and Denmark and Princess Alice of Battenberg, and the widow of Prince Christoph of Hesse.
After consultations with the Foreign Office, Home Office and King George VI's private secretary, Sir Alan Lascelles, a ciphered telegram dated 18 April 1946 and crafted by Sir Albert Napier, permanent secretary to the Lord Chancellor, was transmitted from the British Foreign Office to the Foreign Adviser to the British Commander in Chief at Berlin:


"The Duke of Brunswick has formally applied to The King by letter of March 22nd for the consent of His Majesty under the Act 12 Geo.
11 to the marriage of his son Prince George William with Princess Sophia Dowager Princess of Hesse.
Please convey to the Duke an informal intimation that in view of the fact that a state of war still exists between Great Britain and Germany, His Majesty is advised that the case is not one in which it is practicable for His consent to be given in the manner contemplated by the Act.
"

They had three children: Welf (1947–1981), Georg (born 1949) and Friederike (born 1954).
Ancestry

George William was a descendant of Victoria of the United Kingdom and Albert, Prince Consort through their eldest daughter Victoria, Princess Royal, the wife of Frederick III, German Emperor.
He was born a Prince of the United Kingdom of Great Britain and Ireland.



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
  AssignClass (5498888f-5243-46d1-bda3-5c5ec06d1438)
 Call ID: 5498888f-5243-46d1-bda3-5c5ec06d1438
  Args:
    type: :Man
    source: :GeorgeWilliam
  AssignClass (87c9054b-4d89-451c-92c8-5d0a0ea9ad1e)
 Call ID: 87c9054b-4d89-451c-92c8-5d0a0ea9ad1e
  Args:
    type: :Person
    source: :GeorgeWilliam
  AddLiteral (036b5646-fecf-49fe-9ca1-84ad1851ee73)
 Call ID: 036b5646-fecf-49fe-9ca1-84ad1851ee73
  Args:
    source: :GeorgeWilliam
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1915
  AddLiteral (3f524077-5943-423e-8202-053658f2960e)
 Call ID: 3f524077-5943-423e-8202-053658f2960e
  Args:
    relation: :hasDeathYear
    literal_value: 2006
    literal_type: xsd:integer
    source: :GeorgeWilliam
  AssignClass (7f47b08e-f929-4606-9230-d05e38148078)
 Call ID: 7f47b08e-f929-4606-9230-d05e38148078
  Args:
    type: :Man
    source: :ErnestAugustus
  AssignClass (97589814-9175-4422-b2eb-ec8024f2ef1c)
 Call ID: 97589814-9175-4422-b2eb-ec8024f2ef1c
  Args:
    type: :Person
    source: :ErnestAugustus
  AssignClass (259a78d6-e3e2-4ccf-83a5-2544a5494875)
 Call ID: 259a78d6-e3e2-4ccf-83a5-2544a5494875
  Args:
    type: :Woman
    source: :VictoriaLouise
  AssignClass (31a999fd-a9d0-4eed-a516-659347c56ce3)
 Call ID: 31a999fd-a9d0-4eed-a516-659347c56ce3
  Args:
    type: :Person
    source: :VictoriaLouise
  AddTriple (be0b6c56-357d-4b96-9dcd-3e52162a4994)
 Call ID: be0b6c56-357d-4b96-9dcd-3e52162a4994
  Args:
    source: :GeorgeWilliam
    target: :ErnestAugustus
    relation: :hasFather
  AddTriple (a90518db-bdec-4e2b-adff-f80711f2a37a)
 Call ID: a90518db-bdec-4e2b-adff-f80711f2a37a
  Args:
    relation: :hasMother
    source: :GeorgeWilliam
    target: :VictoriaLouise
  AssignClass (b9978ffa-6227-45d3-bc4c-f5c4db99ad64)
 Call ID: b9978ffa-6227-45d3-bc4c-f5c4db99ad64
  Args:
    type: :Man
    source: :WilhelmII
  AssignClass (068e7a9e-edd0-4c76-b18f-da8a7823f135)
 Call ID: 068e7a9e-edd0-4c76-b18f-da8a7823f135
  Args:
    type: :Person
    source: :WilhelmII
  AssignClass (71f7ad02-1f4f-4bbc-ad3d-3f4386dd7513)
 Call ID: 71f7ad02-1f4f-4bbc-ad3d-3f4386dd7513
  Args:
    type: :Woman
    source: :AugustaVictoria
  AssignClass (96437ee4-34ec-4706-936f-5fc289083aa6)
 Call ID: 96437ee4-34ec-4706-936f-5fc289083aa6
  Args:
    type: :Person
    source: :AugustaVictoria
  AddTriple (a9be17b8-1cd2-4c41-b236-cd44761e49aa)
 Call ID: a9be17b8-1cd2-4c41-b236-cd44761e49aa
  Args:
    relation: :hasFather
    source: :VictoriaLouise
    target: :WilhelmII
  AddTriple (18a17155-46c2-4350-ab6d-fda37fc2b3b7)
 Call ID: 18a17155-46c2-4350-ab6d-fda37fc2b3b7
  Args:
    source: :VictoriaLouise
    target: :AugustaVictoria
    relation: :hasMother
  AssignClass (437de0d6-cd03-45e5-a489-3ba4a1b1fc23)
 Call ID: 437de0d6-cd03-45e5-a489-3ba4a1b1fc23
  Args:
    type: :Woman
    source: :Frederica
  AssignClass (a916b268-e770-4c66-a713-59fb88133322)
 Call ID: a916b268-e770-4c66-a713-59fb88133322
  Args:
    type: :Person
    source: :Frederica
  AddTriple (bf82fa33-c6e9-4b4c-8db9-4e3f7e633800)
 Call ID: bf82fa33-c6e9-4b4c-8db9-4e3f7e633800
  Args:
    target: :Frederica
    source: :GeorgeWilliam
    relation: :hasSister
  AssignClass (f07fa902-2c24-4e70-9c53-9d29e88bff76)
 Call ID: f07fa902-2c24-4e70-9c53-9d29e88bff76
  Args:
    type: :Woman
    source: :Sophie
  AssignClass (02299b85-1e3c-4286-85a7-1edfd94e4ee9)
 Call ID: 02299b85-1e3c-4286-85a7-1edfd94e4ee9
  Args:
    type: :Person
    source: :Sophie
  AddTriple (9e630c2b-fe02-459c-b1fe-3f152781334f)
 Call ID: 9e630c2b-fe02-459c-b1fe-3f152781334f
  Args:
    source: :GeorgeWilliam
    target: :Sophie
    relation: :hasRelation
  AddLiteral (e728d78b-af56-45eb-a051-2094830cce15)
 Call ID: e728d78b-af56-45eb-a051-2094830cce15
  Args:
    literal_value: 1946
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :GeorgeWilliam
  AssignClass (3ab169fc-20b8-4e0c-bac6-fd8cc67e0009)
 Call ID: 3ab169fc-20b8-4e0c-bac6-fd8cc67e0009
  Args:
    type: :Man
    source: :AndrewOfGreece
  AssignClass (423c4c18-f7bd-4b3a-b4ee-1b5b7280cd60)
 Call ID: 423c4c18-f7bd-4b3a-b4ee-1b5b7280cd60
  Args:
    type: :Person
    source: :AndrewOfGreece
  AssignClass (67c3b278-ca74-4a1d-9267-a454d09e7fba)
 Call ID: 67c3b278-ca74-4a1d-9267-a454d09e7fba
  Args:
    type: :Woman
    source: :AliceOfBattenberg
  AssignClass (52a417bd-b78b-4c79-b671-ec69c9e6d172)
 Call ID: 52a417bd-b78b-4c79-b671-ec69c9e6d172
  Args:
    type: :Person
    source: :AliceOfBattenberg
  AddTriple (c015c364-c780-4c60-a9ec-851a20bb04de)
 Call ID: c015c364-c780-4c60-a9ec-851a20bb04de
  Args:
    relation: :hasFather
    source: :Sophie
    target: :AndrewOfGreece
  AddTriple (64d0c954-a2d3-44b4-ae98-80e7ae035953)
 Call ID: 64d0c954-a2d3-44b4-ae98-80e7ae035953
  Args:
    relation: :hasMother
    source: :Sophie
    target: :AliceOfBattenberg
  AssignClass (80b554ec-b670-4f70-92e7-a1b28083cb2c)
 Call ID: 80b554ec-b670-4f70-92e7-a1b28083cb2c
  Args:
    type: :Man
    source: :Welf
  AssignClass (9b36c016-a739-4360-b369-999c72ac10a2)
 Call ID: 9b36c016-a739-4360-b369-999c72ac10a2
  Args:
    type: :Person
    source: :Welf
  AssignClass (f71401c0-69ce-4e69-a066-583383906e47)
 Call ID: f71401c0-69ce-4e69-a066-583383906e47
  Args:
    type: :Man
    source: :Georg
  AssignClass (2317ab3d-9dff-49dc-863c-fbfc01877274)
 Call ID: 2317ab3d-9dff-49dc-863c-fbfc01877274
  Args:
    type: :Person
    source: :Georg
  AssignClass (2c48ec14-e1ff-45a5-88ad-846b8d947527)
 Call ID: 2c48ec14-e1ff-45a5-88ad-846b8d947527
  Args:
    type: :Woman
    source: :Friederike
  AssignClass (9e60bda2-9aa8-4965-ba88-e00ec38b9ebb)
 Call ID: 9e60bda2-9aa8-4965-ba88-e00ec38b9ebb
  Args:
    type: :Person
    source: :Friederike
  AddTriple (cc708918-a366-40ff-b393-e3c149fdaf01)
 Call ID: cc708918-a366-40ff-b393-e3c149fdaf01
  Args:
    source: :GeorgeWilliam
    target: :Welf
    relation: :hasChild
  AddTriple (2e32acb1-2f95-4e1e-ad50-b4b648b616e1)
 Call ID: 2e32acb1-2f95-4e1e-ad50-b4b648b616e1
  Args:
    relation: :hasChild
    target: :Georg
    source: :GeorgeWilliam
  AddTriple (8208affa-0074-4aa7-a1db-396d2ff4cdd1)
 Call ID: 8208affa-0074-4aa7-a1db-396d2ff4cdd1
  Args:
    relation: :hasChild
    target: :Friederike
    source: :GeorgeWilliam
  AddTriple (02b39ce2-cbe8-4096-a5eb-fb09df8341c7)
 Call ID: 02b39ce2-cbe8-4096-a5eb-fb09df8341c7
  Args:
    source: :Sophie
    target: :Welf
    relation: :hasChild
  AddTriple (7a4e52bf-67d2-4ddd-bf95-1c049143dc73)
 Call ID: 7a4e52bf-67d2-4ddd-bf95-1c049143dc73
  Args:
    target: :Georg
    source: :Sophie
    relation: :hasChild
  AddTriple (2ec67af6-a8ec-4ab7-b11e-91979ba3af08)
 Call ID: 2ec67af6-a8ec-4ab7-b11e-91979ba3af08
  Args:
    source: :Sophie
    target: :Friederike
    relation: :hasChild
  Finish (703b0978-f97a-4e34-b189-06be11baf7cd)
 Call ID: 703b0978-f97a-4e34-b189-06be11baf7cd
  Args: