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
Leopold IV, Prince of Lippe (Leopold Julius Bernhard Adalbert Otto Karl Gustav; 30 May 1871 – 30 December 1949) was the final sovereign of the Principality of Lippe in northwestern Germany from 1905 until his abdication in 1918.
He was the first and only ruler of Lippe of the Lippe-Biesterfeld branch.
Early life

He was born as Count Leopold of Lippe-Biesterfeld in Oberkassel, the son of Ernest, Count of Lippe-Biesterfeld and Countess Karoline of Wartensleben.
Leopold belonged to the Lippe-Biesterfeld line of the House of Lippe which was the most senior line of the princely house after the reigning Lippe-Detmold line.
Ruler of Lippe

Since 1895, the Principality of Lippe had been ruled by a regent due to the incapacity of Prince Alexander.
Leopold's father had acted as regent since 1897, and following his death on 26 September 1904, Leopold assumed the regency.
This was not recognized by the German Emperor Wilhelm II, who initially refused to legally recognize Leopold as regent as there was an issue over whether Leopold and his siblings were of legitimate rank, and as such eligible for the succession.
As a result, the Diet of Lippe appointed a high commission to consider the matter.
The regency issue was still ongoing when Prince Alexander died on 13 January 1905.
Leopold was confirmed as Prince of Lippe and Alexander's successor on 25 October 1905, following a court ruling.
On 3 June 1911, while out motoring, Leopold and his brother Prince Julius were attacked by a gang of Italian laborers who hurled a shower of missiles at the princes.
Though Leopold escaped unhurt, his brother received a head wound.
During World War I, Leopold upgraded the titles of the various lines of the House of Lippe.
One of the members to benefit from the granting of titles was Leopold's nephew Count Bernhard of Biesterfeld (son of Leopold's brother Bernhard), who would go on to become the Prince Consort of Queen Juliana of the Netherlands.
On 24 February 1916, Bernhard and his brother were upgraded to the title Prince of Lippe-Biesterfeld with the style Serene Highness.
The Counts of Lippe-Weissenfeld also benefited with creations of the title Prince of Lippe-Weissenfeld, with the style Serene Highness, taking place on 24 February 1916 for Count Clemens and his descendants, and again on 9 November 1918 for the other members of this line.
Just three days after upgrading the titles of members of the Lippe-Weissenfeld line, and following the German Empire's defeat in World War I and the subsequent revolution, Leopold was forced to renounce the throne on 12 November 1918.
Following the end of his rule, the Principality of Lippe was transformed into a Free state in the new Weimar Republic.
His eldest son the Hereditary Prince Ernst is reported to have been the first German prince to join the party when he signed up in May 1928.
In addition to being pro Nazi, both Hereditary Prince Ernst and Prince Chlodwig had contracted unequal marriages.
So in 1947 when Leopold wrote his will, Armin, his youngest son and only child with his second wife, would succeed him as head of the House of Lippe and also become administrator of the princely family's properties such as Schloss Detmold.
Thus when Leopold died in Detmold his three eldest sons were all disinherited and his youngest son Armin became head of the princely house.
Marriages and children

Leopold was married to Princess Bertha of Hesse-Philippsthal-Barchfeld (1874–1919) on 16 August 1901 in Rotenburg.



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
  AssignClass (3fdd6dac-43ce-4f9d-9f19-e5bd26944673)
 Call ID: 3fdd6dac-43ce-4f9d-9f19-e5bd26944673
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Man
  AssignClass (32972bd5-1fd0-4358-8894-22cd705051fe)
 Call ID: 32972bd5-1fd0-4358-8894-22cd705051fe
  Args:
    type: :Person
    source: Leopold_IV_Prince_of_Lippe
  AddLiteral (421671e5-4977-4c9d-ab4d-85b68a2326fb)
 Call ID: 421671e5-4977-4c9d-ab4d-85b68a2326fb
  Args:
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1871
  AddLiteral (48788f77-ba24-4565-98d0-5c43acfa611d)
 Call ID: 48788f77-ba24-4565-98d0-5c43acfa611d
  Args:
    relation: :hasDeathYear
    literal_value: 1949
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
  AssignClass (c3fa3aeb-ef18-409e-b304-518e29bc35e4)
 Call ID: c3fa3aeb-ef18-409e-b304-518e29bc35e4
  Args:
    type: :Man
    source: Ernest_Count_of_Lippe-Biesterfeld
  AssignClass (5594c237-2866-4400-a31d-92a0ae0cec23)
 Call ID: 5594c237-2866-4400-a31d-92a0ae0cec23
  Args:
    source: Ernest_Count_of_Lippe-Biesterfeld
    type: :Person
  AssignClass (e5816ca1-77a1-41a1-a486-42f48770a5ec)
 Call ID: e5816ca1-77a1-41a1-a486-42f48770a5ec
  Args:
    source: Karoline_of_Wartensleben
    type: :Woman
  AssignClass (aa01f706-141c-419f-a7d0-ccc7864a3dd4)
 Call ID: aa01f706-141c-419f-a7d0-ccc7864a3dd4
  Args:
    source: Karoline_of_Wartensleben
    type: :Person
  AddTriple (8f336c07-de3b-42e3-94e9-c2754060cbea)
 Call ID: 8f336c07-de3b-42e3-94e9-c2754060cbea
  Args:
    source: Leopold_IV_Prince_of_Lippe
    target: Ernest_Count_of_Lippe-Biesterfeld
    relation: :hasFather
  AddTriple (96b309a3-1f2f-4d29-99d7-7ed3ab0f9137)
 Call ID: 96b309a3-1f2f-4d29-99d7-7ed3ab0f9137
  Args:
    relation: :hasMother
    target: Karoline_of_Wartensleben
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (e98a061f-9b9e-47b3-acd0-d58976201d39)
 Call ID: e98a061f-9b9e-47b3-acd0-d58976201d39
  Args:
    source: Julius_Prince_of_Lippe
    type: :Man
  AssignClass (3749a2c9-51ad-48dc-811e-57349bc2a7f4)
 Call ID: 3749a2c9-51ad-48dc-811e-57349bc2a7f4
  Args:
    source: Julius_Prince_of_Lippe
    type: :Person
  AddTriple (affc1f0f-e362-4bf9-8284-0ba1de3af52f)
 Call ID: affc1f0f-e362-4bf9-8284-0ba1de3af52f
  Args:
    target: Leopold_IV_Prince_of_Lippe
    source: Julius_Prince_of_Lippe
    relation: :isBrotherOf
  AssignClass (ebb8548c-cdb3-46a1-8bab-b38776e15618)
 Call ID: ebb8548c-cdb3-46a1-8bab-b38776e15618
  Args:
    source: Bernhard_of_Biesterfeld_brother_of_Leopold
    type: :Man
  AssignClass (44cc85d1-32d1-4eba-973d-fb3baf330fbf)
 Call ID: 44cc85d1-32d1-4eba-973d-fb3baf330fbf
  Args:
    source: Bernhard_of_Biesterfeld_brother_of_Leopold
    type: :Person
  AddTriple (310cfc60-4730-4c8e-b9ca-fcf083157c35)
 Call ID: 310cfc60-4730-4c8e-b9ca-fcf083157c35
  Args:
    source: Bernhard_of_Biesterfeld_brother_of_Leopold
    target: Leopold_IV_Prince_of_Lippe
    relation: :isBrotherOf
  AssignClass (0b9b4829-6c7e-4263-bfc1-6a2d58a5b7b8)
 Call ID: 0b9b4829-6c7e-4263-bfc1-6a2d58a5b7b8
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    type: :Man
  AssignClass (35866f80-1a15-4659-9f8f-90a5e330430c)
 Call ID: 35866f80-1a15-4659-9f8f-90a5e330430c
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    type: :Person
  AddTriple (40560c67-e08f-489a-887e-322eea4bac05)
 Call ID: 40560c67-e08f-489a-887e-322eea4bac05
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    target: Bernhard_of_Biesterfeld_brother_of_Leopold
    relation: :hasFather
  AssignClass (d4d1659a-ac17-49e6-9081-a462d7844947)
 Call ID: d4d1659a-ac17-49e6-9081-a462d7844947
  Args:
    type: :Man
    source: Ernst_Hereditary_Prince_of_Lippe
  AssignClass (defe74bd-6cb9-45bd-940f-4ba9ff1171b0)
 Call ID: defe74bd-6cb9-45bd-940f-4ba9ff1171b0
  Args:
    type: :Person
    source: Ernst_Hereditary_Prince_of_Lippe
  AddTriple (6adaabcc-df8e-43a4-977b-1a9cba170599)
 Call ID: 6adaabcc-df8e-43a4-977b-1a9cba170599
  Args:
    target: Leopold_IV_Prince_of_Lippe
    source: Ernst_Hereditary_Prince_of_Lippe
    relation: :isSonOf
  AssignClass (63caea7f-7cdb-4bd7-9753-82aa6e09cc6f)
 Call ID: 63caea7f-7cdb-4bd7-9753-82aa6e09cc6f
  Args:
    source: Chlodwig_Prince_of_Lippe
    type: :Man
  AssignClass (2831f206-a40d-4d89-9dd3-bc3832fcdd5e)
 Call ID: 2831f206-a40d-4d89-9dd3-bc3832fcdd5e
  Args:
    type: :Person
    source: Chlodwig_Prince_of_Lippe
  AddTriple (5bea1e5a-98e1-4532-b9a7-c48b44f26f28)
 Call ID: 5bea1e5a-98e1-4532-b9a7-c48b44f26f28
  Args:
    source: Chlodwig_Prince_of_Lippe
    target: Leopold_IV_Prince_of_Lippe
    relation: :isSonOf
  AssignClass (d50d65c3-5a50-4ad1-84aa-a86adfc2097d)
 Call ID: d50d65c3-5a50-4ad1-84aa-a86adfc2097d
  Args:
    type: :Man
    source: Armin_Prince_of_Lippe
  AssignClass (806ad474-6405-4f48-bd70-58fd78d45f36)
 Call ID: 806ad474-6405-4f48-bd70-58fd78d45f36
  Args:
    source: Armin_Prince_of_Lippe
    type: :Person
  AddTriple (25b1a976-b50f-4eb2-89c5-9425fcacd70b)
 Call ID: 25b1a976-b50f-4eb2-89c5-9425fcacd70b
  Args:
    relation: :isSonOf
    target: Leopold_IV_Prince_of_Lippe
    source: Armin_Prince_of_Lippe
  AssignClass (21d49f07-af1d-4ce5-b52d-5b2595f93aa1)
 Call ID: 21d49f07-af1d-4ce5-b52d-5b2595f93aa1
  Args:
    type: :Woman
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
  AssignClass (073f4f51-96c4-4640-89c2-8da41708fb8d)
 Call ID: 073f4f51-96c4-4640-89c2-8da41708fb8d
  Args:
    type: :Person
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (569f912b-3696-4c83-8d9f-0c0c74b0ac29)
 Call ID: 569f912b-3696-4c83-8d9f-0c0c74b0ac29
  Args:
    relation: :hasBirthYear
    literal_value: 1874
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_type: xsd:integer
  AddLiteral (0ed6bc48-1db2-4adc-b243-0ed5ce072e2c)
 Call ID: 0ed6bc48-1db2-4adc-b243-0ed5ce072e2c
  Args:
    relation: :hasDeathYear
    literal_value: 1919
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_type: xsd:integer
  AddTriple (381473aa-56f5-4f1d-8061-1e6308403033)
 Call ID: 381473aa-56f5-4f1d-8061-1e6308403033
  Args:
    relation: :hasRelation
    source: Leopold_IV_Prince_of_Lippe
    target: Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (2c438062-ed25-4ed3-a498-8d48349f4dd5)
 Call ID: 2c438062-ed25-4ed3-a498-8d48349f4dd5
  Args:
    relation: :hasMarriageYear
    literal_value: 1901
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
  Finish (6fb9f1bf-bcdf-42af-9200-1ba50e701487)
 Call ID: 6fb9f1bf-bcdf-42af-9200-1ba50e701487
  Args: