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
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (d276dd02-d8d1-4552-b01e-1998473882d9)
 Call ID: d276dd02-d8d1-4552-b01e-1998473882d9
  Args:
    source: :GeorgeWilliamOfHanover
    type: :Man
  AssignClass (70ce7e84-ee77-423b-8a6a-d6233420f710)
 Call ID: 70ce7e84-ee77-423b-8a6a-d6233420f710
  Args:
    source: :GeorgeWilliamOfHanover
    type: :Person
  AddLiteral (c7e131de-00b2-4b86-b9a1-5287fd8e0165)
 Call ID: c7e131de-00b2-4b86-b9a1-5287fd8e0165
  Args:
    literal_type: xsd:integer
    source: :GeorgeWilliamOfHanover
    relation: :hasBirthYear
    literal_value: 1915
  AddLiteral (9c60839a-c8dc-4da9-849b-f706fe7b021b)
 Call ID: 9c60839a-c8dc-4da9-849b-f706fe7b021b
  Args:
    literal_type: xsd:integer
    literal_value: 2006
    relation: :hasDeathYear
    source: :GeorgeWilliamOfHanover
  AssignClass (66992756-52d8-4e74-81f8-1be9d2073785)
 Call ID: 66992756-52d8-4e74-81f8-1be9d2073785
  Args:
    source: :ErnestAugustusDukeOfBrunswick
    type: :Man
  AssignClass (b1917475-1e85-4afb-a41d-b6d79143ab55)
 Call ID: b1917475-1e85-4afb-a41d-b6d79143ab55
  Args:
    type: :Person
    source: :ErnestAugustusDukeOfBrunswick
  AssignClass (fca6e36f-79c7-4535-bd1c-661f6d3ee698)
 Call ID: fca6e36f-79c7-4535-bd1c-661f6d3ee698
  Args:
    source: :VictoriaLouiseOfPrussia
    type: :Woman
  AssignClass (5d4e12ad-72ef-46d1-ad9f-be5c17cead79)
 Call ID: 5d4e12ad-72ef-46d1-ad9f-be5c17cead79
  Args:
    type: :Person
    source: :VictoriaLouiseOfPrussia
  AddTriple (8a58e00b-7652-4af8-b5e4-00607cabf818)
 Call ID: 8a58e00b-7652-4af8-b5e4-00607cabf818
  Args:
    target: :ErnestAugustusDukeOfBrunswick
    relation: :hasFather
    source: :GeorgeWilliamOfHanover
  AddTriple (86421900-0a59-4046-a4bc-fdc15f84ab37)
 Call ID: 86421900-0a59-4046-a4bc-fdc15f84ab37
  Args:
    target: :VictoriaLouiseOfPrussia
    relation: :hasMother
    source: :GeorgeWilliamOfHanover
  AssignClass (b437d3d2-b9c1-48a9-b9c4-4ea18707bb65)
 Call ID: b437d3d2-b9c1-48a9-b9c4-4ea18707bb65
  Args:
    source: :WilhelmII
    type: :Man
  AssignClass (47992a5d-92e4-465e-891f-ffee09001623)
 Call ID: 47992a5d-92e4-465e-891f-ffee09001623
  Args:
    source: :WilhelmII
    type: :Person
  AssignClass (36c9f624-1390-4e09-91c9-07e59c727211)
 Call ID: 36c9f624-1390-4e09-91c9-07e59c727211
  Args:
    source: :AugustaVictoriaOfSchleswigHolstein
    type: :Woman
  AssignClass (36297114-6896-432b-9039-911ca8306fda)
 Call ID: 36297114-6896-432b-9039-911ca8306fda
  Args:
    source: :AugustaVictoriaOfSchleswigHolstein
    type: :Person
  AddTriple (742dd6bb-c4ad-4144-8848-95409a4c33f8)
 Call ID: 742dd6bb-c4ad-4144-8848-95409a4c33f8
  Args:
    source: :VictoriaLouiseOfPrussia
    relation: :hasFather
    target: :WilhelmII
  AddTriple (b9edc709-92e1-4be4-a42c-9e198f2bd136)
 Call ID: b9edc709-92e1-4be4-a42c-9e198f2bd136
  Args:
    source: :VictoriaLouiseOfPrussia
    relation: :hasMother
    target: :AugustaVictoriaOfSchleswigHolstein
  AssignClass (43793543-b43f-4773-a1c9-f1655143b5bd)
 Call ID: 43793543-b43f-4773-a1c9-f1655143b5bd
  Args:
    source: :SophieOfGreeceAndDenmark
    type: :Woman
  AssignClass (af39c57a-233c-4a27-a1fd-10793d07e1a9)
 Call ID: af39c57a-233c-4a27-a1fd-10793d07e1a9
  Args:
    source: :SophieOfGreeceAndDenmark
    type: :Person
  AddTriple (f1a47b40-6d29-45a7-92e5-cb842bc5b5c3)
 Call ID: f1a47b40-6d29-45a7-92e5-cb842bc5b5c3
  Args:
    target: :SophieOfGreeceAndDenmark
    source: :GeorgeWilliamOfHanover
    relation: :hasRelation
  AddLiteral (d0c8b96b-3dad-4b16-8c01-54710719fe0d)
 Call ID: d0c8b96b-3dad-4b16-8c01-54710719fe0d
  Args:
    literal_type: xsd:integer
    source: :GeorgeWilliamOfHanover
    literal_value: 1946
    relation: :hasMarriageYear
  AssignClass (e840339d-509c-448b-aac8-2b7abe65d20c)
 Call ID: e840339d-509c-448b-aac8-2b7abe65d20c
  Args:
    type: :Man
    source: :PrincePhilipDukeOfEdinburgh
  AssignClass (f508f046-aec8-4301-afb3-09c0c9f883c5)
 Call ID: f508f046-aec8-4301-afb3-09c0c9f883c5
  Args:
    type: :Person
    source: :PrincePhilipDukeOfEdinburgh
  AddTriple (b42450b7-f35c-4573-8f15-3fffa7e7d74f)
 Call ID: b42450b7-f35c-4573-8f15-3fffa7e7d74f
  Args:
    source: :SophieOfGreeceAndDenmark
    relation: :isSisterOf
    target: :PrincePhilipDukeOfEdinburgh
  AssignClass (2ca83523-8015-45f6-94a8-0f91680c27cf)
 Call ID: 2ca83523-8015-45f6-94a8-0f91680c27cf
  Args:
    source: :FredericaQueenOfTheHellenes
    type: :Woman
  AssignClass (33cc9aae-592b-48ec-94f5-2df2bace9a08)
 Call ID: 33cc9aae-592b-48ec-94f5-2df2bace9a08
  Args:
    type: :Person
    source: :FredericaQueenOfTheHellenes
  AddTriple (002652c7-1a4e-4cf0-a29a-ede2fa189821)
 Call ID: 002652c7-1a4e-4cf0-a29a-ede2fa189821
  Args:
    relation: :isSisterOf
    source: :FredericaQueenOfTheHellenes
    target: :GeorgeWilliamOfHanover
  AssignClass (c79768c1-74c7-4720-92f7-f9222bc9f46c)
 Call ID: c79768c1-74c7-4720-92f7-f9222bc9f46c
  Args:
    source: :KingPaulOfGreece
    type: :Man
  AssignClass (1679a59f-54a2-4861-bd74-6f9b107ba300)
 Call ID: 1679a59f-54a2-4861-bd74-6f9b107ba300
  Args:
    type: :Person
    source: :KingPaulOfGreece
  AddTriple (634b48f4-63f6-44d9-b187-822ece6aec1c)
 Call ID: 634b48f4-63f6-44d9-b187-822ece6aec1c
  Args:
    target: :KingPaulOfGreece
    relation: :hasRelation
    source: :FredericaQueenOfTheHellenes
  AssignClass (a4d953ee-9534-4321-9172-d388a5f73e86)
 Call ID: a4d953ee-9534-4321-9172-d388a5f73e86
  Args:
    type: :Man
    source: :Welf
  AssignClass (8b720b93-4a39-4d4b-a449-a8742ec23f60)
 Call ID: 8b720b93-4a39-4d4b-a449-a8742ec23f60
  Args:
    source: :Welf
    type: :Person
  AssignClass (31a4f307-271d-40b6-938c-6bf8cb9c4fab)
 Call ID: 31a4f307-271d-40b6-938c-6bf8cb9c4fab
  Args:
    source: :Georg
    type: :Man
  AssignClass (9ecaefe8-13fb-46c8-becc-c1eb2495f644)
 Call ID: 9ecaefe8-13fb-46c8-becc-c1eb2495f644
  Args:
    type: :Person
    source: :Georg
  AssignClass (0b9f2a2c-ff91-4f27-8f68-c56afa8fee29)
 Call ID: 0b9f2a2c-ff91-4f27-8f68-c56afa8fee29
  Args:
    source: :Friederike
    type: :Woman
  AssignClass (e06dfedf-7526-438f-a288-2df28e968f5c)
 Call ID: e06dfedf-7526-438f-a288-2df28e968f5c
  Args:
    type: :Person
    source: :Friederike
  AddTriple (cb184b5d-ef2e-4fb7-aad6-7e964a563ae9)
 Call ID: cb184b5d-ef2e-4fb7-aad6-7e964a563ae9
  Args:
    relation: :hasChild
    source: :GeorgeWilliamOfHanover
    target: :Welf
  AddTriple (78724bbd-5a9b-4ec2-94f1-ff725dff8954)
 Call ID: 78724bbd-5a9b-4ec2-94f1-ff725dff8954
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasChild
    target: :Georg
  AddTriple (3a39828c-f415-4119-a7ee-d0d0db875bb6)
 Call ID: 3a39828c-f415-4119-a7ee-d0d0db875bb6
  Args:
    source: :GeorgeWilliamOfHanover
    relation: :hasChild
    target: :Friederike
  AddTriple (466e3de1-313a-43c6-8340-1b683f281a20)
 Call ID: 466e3de1-313a-43c6-8340-1b683f281a20
  Args:
    relation: :hasChild
    source: :SophieOfGreeceAndDenmark
    target: :Welf
  AddTriple (8f982755-727f-42e6-ba50-6b0c450d3e5d)
 Call ID: 8f982755-727f-42e6-ba50-6b0c450d3e5d
  Args:
    target: :Georg
    relation: :hasChild
    source: :SophieOfGreeceAndDenmark
  AddTriple (ca99e93f-6e23-454a-aaa8-b688d7fbb599)
 Call ID: ca99e93f-6e23-454a-aaa8-b688d7fbb599
  Args:
    relation: :hasChild
    source: :SophieOfGreeceAndDenmark
    target: :Friederike
  AssignClass (1ebc6cda-f3ad-497e-a0f7-1818c0fb55dc)
 Call ID: 1ebc6cda-f3ad-497e-a0f7-1818c0fb55dc
  Args:
    source: :PrinceAndrewOfGreeceAndDenmark
    type: :Man
  AssignClass (c8e4400f-f0ac-41c4-8211-898c49ea80ca)
 Call ID: c8e4400f-f0ac-41c4-8211-898c49ea80ca
  Args:
    type: :Person
    source: :PrinceAndrewOfGreeceAndDenmark
  AssignClass (65c2a2aa-f7f6-422a-b084-3a25b61f9445)
 Call ID: 65c2a2aa-f7f6-422a-b084-3a25b61f9445
  Args:
    type: :Woman
    source: :PrincessAliceOfBattenberg
  AssignClass (2f23ec52-d1a0-4d7c-9abf-d1c06d91e858)
 Call ID: 2f23ec52-d1a0-4d7c-9abf-d1c06d91e858
  Args:
    type: :Person
    source: :PrincessAliceOfBattenberg
  AddTriple (4ff3f0dd-7b70-4bc8-9cb5-b7cea1c2a9be)
 Call ID: 4ff3f0dd-7b70-4bc8-9cb5-b7cea1c2a9be
  Args:
    target: :PrinceAndrewOfGreeceAndDenmark
    relation: :hasFather
    source: :SophieOfGreeceAndDenmark
  AddTriple (47868b8e-eb1d-494a-9396-e7921996bf94)
 Call ID: 47868b8e-eb1d-494a-9396-e7921996bf94
  Args:
    target: :PrincessAliceOfBattenberg
    relation: :hasMother
    source: :SophieOfGreeceAndDenmark
  Finish (28fafebe-9c03-4cad-afc2-f2d2a2f7f9c9)
 Call ID: 28fafebe-9c03-4cad-afc2-f2d2a2f7f9c9
  Args: