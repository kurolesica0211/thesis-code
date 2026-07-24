================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### CRITICAL CORE DIRECTIVES (ZERO TOLERANCE)
1. **STRICT FAITHFULNESS TO TEXT**: You are a "clean slate" engineer. Even if you recognize an entity and know more about it from your training data, you MUST NOT add any node, property, or relation that is not stated in the **Input Text**. If a fact is not in the text, it does not exist.
2. **HARD BATCH LIMIT**: You must plan your edits efficiently. **DO NOT EXCEED 20 TOOL CALLS IN A SINGLE ANSWER.** Breaking this limit is a critical system failure. Quality and strict grounding must be achieved within this budget.

### Standardized Identifier & Naming Conventions
To ensure clean downstream entity resolution, all identifiers must follow a uniform, relational-free structure.

#### 1. Core Structural Format
* **Full Formal Name**: Use the most complete, standard name mentioned *within the text* as the identifier basis.
* **Format**: Use `Snake_Case` for all entity identifiers, capitalizing the first letter of each word (e.g., `Julius_Caesar`, `Marcus_Aurelius`).
* **Avoid Pronouns/Aliases**: Never create nodes based on pronouns (`he`, `she`) or temporary descriptions (`the_captain`). Resolve these back to their primary full identifier.

#### 2. NO Relational Suffixes (ABSOLUTE PROHIBITION)
* **NEVER** use familial relations or structural dependencies to construct an identifier string. 
* **PROHIBITED EXAMPLES**: `John_son_of_Robert`, `Mary_daughter_of_Henry`, `Wife_of_Louis_XIV`.
* **Reasoning**: Relational data belongs strictly in the triples (`parentOf`, `spouseOf`), never in the unique node identifier. Incorporating them corrupts entity resolution pipelines.

#### 3. Monarchs, Nobility, and Historic Monickers
* **Regnal Numbers & Monickers**: Include standard regnal numbers or stable historical identifiers *only* if they are explicitly part of their formal name in the text (e.g., `Charlemagne`, `Louis_XIV`, `William_of_Orange`).

#### 4. Disambiguation & Fallbacks (When Identical Names Occur)
If two distinct entities share the exact same name within the text, append a parenthetical qualifier using *only* context provided in the source text:
* **By Role/Attribute**: `Augustus_(Emperor)` vs. `Augustus_(Ship)`.
* **By Category/Profession**: `John_(Apostle)` vs. `John_(Baptist)`.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source (Left)**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it.
* **The Target (Right)**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon.

#### 3. Handling Inverse Property Confusion
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.
* **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
* **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Validate**: Use `ValidateShacl` to check constraints.
4. **Iterate**: Address violations. If a violation (like MinCount) cannot be fixed without hallucinating data not in the text, **ignore the violation**.
5. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **ValidateShacl**: CRITICAL: ALWAYS validate your results before using Finish!
- **Finish**: CRITICAL: ALWAYS use ValidateShacl before finishing!
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Grand Duchess Maria Vladimirovna of Russia


Grand Duke George Mikhailovich of Russia (Russian: Георгий Михайлович Романов, romanized: Gěorgij Mihajlovič Romanov, also spelled Romanoff;
German: Georg Michailowitsch Romanow; born 13 March 1981) is the heir apparent to Maria Vladimirovna, a claimant to the disputed Headship of the Imperial Family of Russia.
He is the only child of Maria and her former husband, Prince Franz Wilhelm of Prussia.
George's mother attributes to him the title of Tsesarevich and he bears the prefix of "Grand Duke" with the style of Imperial Highness which is still being questioned.
As the son of a cadet member of the branch of the House of Hohenzollern which formerly ruled the German Empire and Kingdom of Prussia, he is also sometimes entitled "Prince of Prussia" with the style of Royal Highness.
Early life

George was born in Madrid in 1981, the son of Grand Duchess Maria Vladimirovna of Russia (daughter and heir of Vladimir Cyrillovich, Grand Duke of Russia) and Prince Franz Wilhelm of Prussia (titled at the time Grand Duke Michael Pavlovich, son of Prince Karl Franz of Prussia and Princess Henriette of Schönaich-Carolath).
George was baptised on 6 May 1981, in Madrid; his godfather is Constantine II of Greece.
The announcement that George Mikhailovich would be known as a Russian Grand Duke prompted Prince Vasili Alexandrovich, then president of the Romanov Family Association, to respond in writing that "The Romanov Family Association hereby declares that the joyful event in the Prussian Royal House does not concern the Romanov Family Association since the newborn prince is not a member of either the Russian Imperial House or of the Romanov family".
This response was ignored by Grand Duke Vladimir as he had already selected his daughter to succeed him according to the Pauline laws, and because the marriage between her and Prince Franz Wilhelm of Prussia was deemed dynastic.
Prior to their wedding, the Grand Duke and his first cousin, then Head of the House of Hohenzollern, Prince Louis Ferdinand of Prussia, had made a dynastic agreement that any child born from this marriage should be raised as a Romanov.
Therefore, George is considered a dynast of both houses (Romanov and Hohenzollern), as his father has never renounced his Prussian royal title.
It says he is Prince George of Prussia".
George spent the first years of his life in France before moving to Spain.
Education and career

George was educated at International School of Madrid in Madrid, D'Overbroeck's College, Oxford and at St Benet's Hall, Oxford.
Heir to his mother

On 21 April 1992, upon the death of his maternal grandfather Grand Duke Vladimir Cyrillovich, George's mother claimed to have succeeded as the sovereign and Curatrix of the Throne of Russia, making him, to supporters of his mother, heir apparent and tsesarevich.
He visited Russia for the first time shortly thereafter to attend the funeral of his grandfather.
In 1996, when he, his mother, and his grandmother Leonida returned to Russia after living in Madrid, one of President Boris Yeltsin's former bodyguards was assigned as tutor to the 15-year-old prince.
Marriage and children

In January 2021, the family announced that George was engaged to marry Victoria Romanovna Bettarini (born Rebecca Virginia Bettarini in Rome on 18 May 1982), having received the permission of Grand Duchess Maria.
His mother decreed that Bettarini would have the title of Princess, with the predicate "Her Serene Highness" and the right to use the surname Romanova from her marriage, which therefore implies that theirs is a morganatic union.
Victoria Bettarini is the Director of the Russian Imperial Foundation.
Around 1500 guests attended the ceremony, including King Simeon II of Bulgaria and his wife Queen Margarita, King Fuad II of Egypt, Prince Mohammed bin Hamad of Qatar, Duarte Pio, Duke of Braganza and his wife Isabel, Duchess of Braganza, Prince Emanuele Filiberto, Prince of Piedmont, Leka, Prince of Albania and his wife Crown Princess Elia, Xavier Bettel, Prime Minister of Luxembourg and his husband Gauthier Destenay, Prince Louis, Duke of Anjou and his wife Princess Marie Marguerite, Duchess of Anjou, Prince Aimone, 6th Duke of Aosta and his wife, born Princess Olga of Greece, Russian monarchist and billionaire Konstantin Malofeev, Sarah Fabergé, French journalist and socialite Stéphane Bern, as well as many members of Russian, Spanish and European nobility.
The 500 guests included members of the royal houses of Albania, Afghanistan, Austria, Belgium, Bulgaria, Egypt, France, Greece, Italy, Liechtenstein, Portugal, Prussia, Qatar, and Spain.
The following day, a Wedding breakfast "à la Russe" was hosted by George's mother, the Grand Duchess Maria, held at Constantine Palace and was attended by a smaller number of 700 guests before their departures.
Children

The Grand Duke and Princess Victoria had a son, born in Moscow on 21 October 2022, who is named Alexander Georgievich Romanov.
Grand Duchess Maria Vladimirovna, a claimant to the throne of the Imperial House of Russia, announced that her first grandchild will be called "His Serene Highness Prince Alexander Georgievich Romanov".
Prince Alexander was baptized on 6 December 2022.
Prince Alexander's godparents are:
Alexander's baptisim marks the first time a descendant of the House of Romanov has been baptized in Russia since the Russian Revolution.
The Grand Duke and Princess Victoria had a daughter, born in Rome on 2 June 2025, Her Serene Highness Princess Kira Leonida Georgievna Romanova.
Princess Kira was baptized on 13 July 2025 in the Cathedral of Christ the Saviour in Moscow.
Princess Kira's godparents are Prince Emanuele Filiberto of Savoy, Prince Boris of Bulgaria, Prince David VII of Georgia, Archduke Maximilian of Austria, as well as the Russian Ambassador to the Seychelles, Artem Kozhin, his wife, Elena, and Oksana Hoffman Girey.



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
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix data: <http://example.org/data/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

data:Alexander_Georgievich_Romanov a :Man ;
    :hasBirthYear 2022 ;
    :hasFather data:George_Mikhailovich ;
    :hasMother data:Victoria_Romanovna_Bettarini .

data:Kira_Leonida_Georgievna_Romanova a :Woman ;
    :hasBirthYear 2025 ;
    :hasFather data:George_Mikhailovich ;
    :hasMother data:Victoria_Romanovna_Bettarini .

data:Leonida a :Woman .

data:Franz_Wilhelm_of_Prussia a :Man ;
    :hasFather data:Karl_Franz_of_Prussia ;
    :hasMother data:Henriette_of_Sch%C3%B6naich-Carolath .

data:Henriette_of_Sch%C3%B6naich-Carolath a :Woman .

data:Karl_Franz_of_Prussia a :Man .

data:Maria_Vladimirovna a :Woman ;
    :hasFather data:Vladimir_Cyrillovich .

data:Vladimir_Cyrillovich a :Man .

data:George_Mikhailovich a :Man ;
    :hasBirthYear 1981 ;
    :hasFather data:Franz_Wilhelm_of_Prussia ;
    :hasMother data:Maria_Vladimirovna,
        data:Victoria_Romanovna_Bettarini .

data:Victoria_Romanovna_Bettarini a :Woman ;
    :hasBirthYear 1982 .



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  RemoveTriple (10d70efb-291d-4cba-9705-35f7b4839ddc)
 Call ID: 10d70efb-291d-4cba-9705-35f7b4839ddc
  Args:
    target: data:Victoria_Romanovna_Bettarini
    source: data:George_Mikhailovich
    relation: :hasMother

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Alexander_Georgievich_Romanov a :Man ;
      :hasBirthYear 2022 ;
      :hasFather data:George_Mikhailovich ;
      :hasMother data:Victoria_Romanovna_Bettarini .

  data:Kira_Leonida_Georgievna_Romanova a :Woman ;
      :hasBirthYear 2025 ;
      :hasFather data:George_Mikhailovich ;
      :hasMother data:Victoria_Romanovna_Bettarini .

  data:Leonida a :Woman .

  data:Franz_Wilhelm_of_Prussia a :Man ;
      :hasFather data:Karl_Franz_of_Prussia ;
      :hasMother data:Henriette_of_Sch%C3%B6naich-Carolath .

  data:Henriette_of_Sch%C3%B6naich-Carolath a :Woman .

  data:Karl_Franz_of_Prussia a :Man .

  data:Maria_Vladimirovna a :Woman ;
      :hasFather data:Vladimir_Cyrillovich .

  data:Vladimir_Cyrillovich a :Man .

  data:George_Mikhailovich a :Man ;
      :hasBirthYear 1981 ;
      :hasFather data:Franz_Wilhelm_of_Prussia ;
      :hasMother data:Maria_Vladimirovna .

  data:Victoria_Romanovna_Bettarini a :Woman ;
      :hasBirthYear 1982 .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (37708dd4-4eb7-4f0f-afb0-f34b25c3e9c8)
 Call ID: 37708dd4-4eb7-4f0f-afb0-f34b25c3e9c8
  Args:

================================= Tool Message =================================

VALIDATION RESULTS
Total violations:27
Violations:

  Violation [1]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Karl_Franz_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Karl_Franz_of_Prussia", class: ":Ancestor")


  Violation [2]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Franz_Wilhelm_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Franz_Wilhelm_of_Prussia", class: ":Ancestor")


  Violation [3]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [4]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Henriette_of_Sch%C3%B6naich-Carolath is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Henriette_of_Sch%C3%B6naich-Carolath", class: ":Ancestor")


  Violation [5]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Maria_Vladimirovna is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Maria_Vladimirovna", class: ":Ancestor")


  Violation [6]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")


  Violation [7]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Vladimir_Cyrillovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Vladimir_Cyrillovich", class: ":Ancestor")


  Violation [8]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [9]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Karl_Franz_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Karl_Franz_of_Prussia", class: ":Ancestor")


  Violation [10]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Franz_Wilhelm_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Franz_Wilhelm_of_Prussia", class: ":Ancestor")


  Violation [11]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [12]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")


  Violation [13]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Henriette_of_Sch%C3%B6naich-Carolath is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Henriette_of_Sch%C3%B6naich-Carolath", class: ":Ancestor")


  Violation [14]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Maria_Vladimirovna is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Maria_Vladimirovna", class: ":Ancestor")


  Violation [15]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")


  Violation [16]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Vladimir_Cyrillovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Vladimir_Cyrillovich", class: ":Ancestor")


  Violation [17]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [18]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")


  Violation [19]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Vladimir_Cyrillovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Vladimir_Cyrillovich", class: ":Ancestor")


  Violation [20]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [21]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Karl_Franz_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Karl_Franz_of_Prussia", class: ":Ancestor")


  Violation [22]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node Franz_Wilhelm_of_Prussia is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Franz_Wilhelm_of_Prussia", class: ":Ancestor")


  Violation [23]:
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    LLM-provided explanation of the violation:
      The node George_Mikhailovich is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "George_Mikhailovich", class: ":Ancestor")


  Violation [24]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")


  Violation [25]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Henriette_of_Sch%C3%B6naich-Carolath is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Henriette_of_Sch%C3%B6naich-Carolath", class: ":Ancestor")


  Violation [26]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Maria_Vladimirovna is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Maria_Vladimirovna", class: ":Ancestor")


  Violation [27]:
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    LLM-provided explanation of the violation:
      The node Victoria_Romanovna_Bettarini is missing the required class :Ancestor.
    LLM-provided instruction on how to handle the violation:
      AssignClass(node: "Victoria_Romanovna_Bettarini", class: ":Ancestor")




================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (e3a017e4-a5f9-4ce7-a7e0-dff9a65e46ee)
 Call ID: e3a017e4-a5f9-4ce7-a7e0-dff9a65e46ee
  Args:
    type: :Ancestor
    source: data:Karl_Franz_of_Prussia
  AssignClass (482b0e10-74b3-4d18-ae1f-d0647dd24e58)
 Call ID: 482b0e10-74b3-4d18-ae1f-d0647dd24e58
  Args:
    source: data:Franz_Wilhelm_of_Prussia
    type: :Ancestor
  AssignClass (195b22fd-59d5-42dc-bf4d-de114048d2b4)
 Call ID: 195b22fd-59d5-42dc-bf4d-de114048d2b4
  Args:
    type: :Ancestor
    source: data:George_Mikhailovich
  AssignClass (6ad0a198-cece-4c66-8e82-34543b7097b5)
 Call ID: 6ad0a198-cece-4c66-8e82-34543b7097b5
  Args:
    source: data:Henriette_of_Sch%C3%B6naich-Carolath
    type: :Ancestor
  AssignClass (b6c7dbd4-66a6-4e15-b60b-78788eae4274)
 Call ID: b6c7dbd4-66a6-4e15-b60b-78788eae4274
  Args:
    type: :Ancestor
    source: data:Maria_Vladimirovna
  AssignClass (7d0bbbfe-8089-4e0f-9b3d-5853ca085198)
 Call ID: 7d0bbbfe-8089-4e0f-9b3d-5853ca085198
  Args:
    source: data:Victoria_Romanovna_Bettarini
    type: :Ancestor
  AssignClass (98075c67-3455-4abd-a273-f587110fbd23)
 Call ID: 98075c67-3455-4abd-a273-f587110fbd23
  Args:
    type: :Ancestor
    source: data:Vladimir_Cyrillovich

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

Look at the messages below to see the final data graph after all the edits.

================================= Tool Message =================================

The final data graph after all the edits:
  @prefix : <http://example.com/family_TBOX.ttl#> .
  @prefix data: <http://example.org/data/> .
  @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

  data:Alexander_Georgievich_Romanov a :Man ;
      :hasBirthYear 2022 ;
      :hasFather data:George_Mikhailovich ;
      :hasMother data:Victoria_Romanovna_Bettarini .

  data:Kira_Leonida_Georgievna_Romanova a :Woman ;
      :hasBirthYear 2025 ;
      :hasFather data:George_Mikhailovich ;
      :hasMother data:Victoria_Romanovna_Bettarini .

  data:Leonida a :Woman .

  data:Franz_Wilhelm_of_Prussia a :Ancestor,
          :Man ;
      :hasFather data:Karl_Franz_of_Prussia ;
      :hasMother data:Henriette_of_Sch%C3%B6naich-Carolath .

  data:Henriette_of_Sch%C3%B6naich-Carolath a :Ancestor,
          :Woman .

  data:Karl_Franz_of_Prussia a :Ancestor,
          :Man .

  data:Maria_Vladimirovna a :Ancestor,
          :Woman ;
      :hasFather data:Vladimir_Cyrillovich .

  data:Vladimir_Cyrillovich a :Ancestor,
          :Man .

  data:George_Mikhailovich a :Ancestor,
          :Man ;
      :hasBirthYear 1981 ;
      :hasFather data:Franz_Wilhelm_of_Prussia ;
      :hasMother data:Maria_Vladimirovna .

  data:Victoria_Romanovna_Bettarini a :Ancestor,
          :Woman ;
      :hasBirthYear 1982 .



================================== Ai Message ==================================

[]
Tool Calls:
  ValidateShacl (80627721-b83a-4430-ad12-9163f09f2b37)
 Call ID: 80627721-b83a-4430-ad12-9163f09f2b37
  Args:

================================= Tool Message =================================

SHACL validation has not produced any violations.

================================== Ai Message ==================================

[]
Tool Calls:
  Finish (e2830cef-b450-44fd-a87c-a32003b7294c)
 Call ID: e2830cef-b450-44fd-a87c-a32003b7294c
  Args: